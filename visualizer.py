import torch
from os import walk, path, makedirs
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import plot_scene
from pytorch3d.renderer import TexturesVertex
from tqdm import tqdm
import matplotlib.pyplot as plt
import reader
from util.utils import color_converter


class Visualizer(object):

    def __init__(self, args):
        self.indir = path.dirname(args.file) if args.in_dir is None else args.in_dir
        self.outdir = path.join(path.dirname(self.indir), 'output') if args.out_dir is None else args.out_dir
        self.filepath = args.file
        self.save = not args.no_save
        self.show = args.show
        self.color_rgb = [args.r, args.g, args.b]
        if args.color is not None:
            self.color_rgb = color_converter(args.color)
        self.th = args.th
        self.verbose = args.verbose
        self.skip_plotted = args.skip_plotted


    def visualize_directory(self):
        fcount = sum(len(files) for _, _, files in walk(self.indir))
        with tqdm(total=fcount) as pbar:
            for (dirpath, _, filenames) in walk(self.indir):
                for filename in filenames:
                    filepath = path.join(dirpath, filename)
                    self.visualize_single_file(filepath)
                    pbar.update(1)

    def visualize_single_file(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
            outpath = path.join(self.outdir, path.basename(filepath))
        else:
            outpath = filepath.replace(self.indir, self.outdir)

        outname, ext = path.splitext(outpath)
        outpath = outname + ".png"

        if self.skip_plotted and path.exists(outpath) and (self.save and not self.show):
            print("Skipping already visualized plot at %s" % outpath)
            return
        
        makedirs(path.dirname(outpath), exist_ok=True)

        if ext == ".off":
            verts, faces = reader.read_off(file_path=filepath)
            self.__visualize_off_or_obj_file(verts, faces, save_path=outpath)
        elif ext == ".obj":
            verts, faces = reader.read_obj(file_path=filepath)
            self.__visualize_off_or_obj_file(verts, faces, save_path=outpath)
        elif ext == ".binvox":
            volume = reader.read_binvox(file_path=filepath)
            self.__visualize_binvox_or_npy_file(volume, save_path=outpath)
        elif ext == ".npy":
            volume = reader.read_npy(file_path=filepath, th=self.th)
            self.__visualize_binvox_or_npy_file(volume, save_path=outpath)
        elif ext == ".glb":
            raise Exception("Work in progress")
        elif ext == ".ply":
            raise Exception("Work in progress")
        else:
            print("Skipping unsupported file %s" % filepath)

        if self.verbose:
            print("Plot saved to %s" % outpath)

    def __visualize_off_or_obj_file(self, verts, faces, save_path=None):
        verts_rgb = torch.Tensor([self.color_rgb] * verts.shape[1]).unsqueeze(dim=0)
        textures = TexturesVertex(verts_features=verts_rgb)
        mesh = Meshes(verts=verts, faces=faces, textures=textures)
        range_ = [torch.max(verts), torch.min(verts)]
        axis_settings = dict(xaxis=dict(visible=False, range=range_, autorange=False),
                             yaxis=dict(visible=False, range=range_, autorange=False),
                             zaxis=dict(visible=False, range=range_, autorange=False))
        fig = plot_scene({
            "": {"mesh": mesh}
        }, **axis_settings)
        fig.update_layout(margin=dict(t=1, r=1, b=1, l=1))

        if self.show:  # show figure
            fig.show()
        if self.save:  # save png
            fig.write_image(save_path)

    def __visualize_binvox_or_npy_file(self, volume, save_path=None):
        ax = plt.figure().add_subplot(projection="3d")
        ax.voxels(volume, facecolors=self.color_rgb, edgecolor="k")
        ax.view_init(elev=160, azim=-20)
        plt.axis("off")

        if self.show:  # show figure
            plt.show()
        if self.save:  # save png
            plt.savefig(save_path, bbox_inches='tight')
            plt.clf()
            plt.close()

    