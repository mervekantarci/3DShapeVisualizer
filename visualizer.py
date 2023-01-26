import torch
from os import walk, path, makedirs
from pytorch3d.structures import Meshes
from pytorch3d.vis.plotly_vis import plot_scene
from pytorch3d.renderer import TexturesVertex
from tqdm import tqdm
import matplotlib.pyplot as plt
import reader


class Visualizer(object):

    def __init__(self, args):
        self.indir = path.dirname(args.file) if args.in_dir is None else args.in_dir
        self.outdir = path.join(path.dirname(self.indir), 'output') if args.out_dir is None else args.out_dir
        self.filepath = args.file
        self.save = args.save
        self.show = args.show
        self.color = [args.r, args.g, args.b]
        self.th = args.th
        self.verbose = args.verbose
        self.skip = args.skip or args.skip_verbose
        self.skip_verbose = args.skip_verbose

    def visualize_off_or_obj_file(self, verts, faces, save_path=None):
        verts_rgb = torch.Tensor([self.color] * verts.shape[1]).unsqueeze(dim=0)
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

    def visualize_binvox_or_npy_file(self, volume, save_path=None):
        ax = plt.figure().add_subplot(projection="3d")
        ax.voxels(volume, facecolors=self.color, edgecolor="k")
        ax.view_init(elev=160, azim=-20)
        plt.axis("off")

        if self.show:  # show figure
            plt.show()
        if self.save:  # save png
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()

    def visualize_single_file(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
            outpath = path.join(self.outdir, path.basename(filepath))
        else:
            outpath = filepath.replace(self.indir, self.outdir)

        if self.skip and path.exists(outpath):
            if self.skip_verbose:
                print("Skipping already visualized plot at %s" % outpath)
            return

        makedirs(path.dirname(outpath), exist_ok=True)

        if filepath.endswith(".off"):
            outpath = outpath.replace(".off", ".png")
            verts, faces = reader.read_off(file_path=filepath)
            self.visualize_off_or_obj_file(verts, faces, save_path=outpath)
        elif filepath.endswith(".obj"):
            outpath = outpath.replace(".obj", ".png")
            verts, faces = reader.read_obj(file_path=filepath)
            self.visualize_off_or_obj_file(verts, faces, save_path=outpath)
        elif filepath.endswith(".binvox"):
            outpath = outpath.replace(".binvox", ".png")
            volume = reader.read_binvox(file_path=filepath)
            self.visualize_binvox_or_npy_file(volume, save_path=outpath)
        elif filepath.endswith(".npy"):
            outpath = outpath.replace(".npy", ".png")
            volume = reader.read_npy(file_path=filepath, th=self.th)
            self.visualize_binvox_or_npy_file(volume, save_path=outpath)
        elif filepath.endswith(".glb"):
            raise Exception("Work in progress")
        elif filepath.endswith(".ply"):
            raise Exception("Work in progress")
        else:
            print("Skipping unsupported file %s" % filepath)

        if self.verbose:
            print("Plot saved to %s" % outpath)

    def visualize_directory(self):
        fcount = sum(len(files) for _, _, files in walk(self.indir))
        with tqdm(total=fcount) as pbar:
            for (dirpath, dirnames, filenames) in walk(self.indir):
                for filename in filenames:
                    filepath = path.join(dirpath, filename)
                    self.visualize_single_file(filepath)
                    pbar.update(1)
