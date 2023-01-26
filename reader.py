import binvox_rw
import torch
from pytorch3d.io import load_obj
import numpy as np


def read_off(file_path):
    file = open(file_path, "r")
    if "OFF" != file.readline().strip():
        raise "File format not correct!"
    n_verts, n_faces, __ = tuple([int(s) for s in file.readline().strip().split(' ')])
    verts = [[float(s) for s in file.readline().strip().split(' ')] for i_vert in range(n_verts)]
    verts = torch.Tensor(verts).unsqueeze(dim=0)
    faces = [[int(s) for s in file.readline().strip().split(' ')][1:] for i_face in range(n_faces)]
    faces = torch.Tensor(faces).unsqueeze(dim=0)
    return verts, faces


def read_obj(file_path):
    verts, faces_idx, _ = load_obj(file_path)
    faces = faces_idx.verts_idx.unsqueeze(dim=0)
    verts = verts.unsqueeze(dim=0)
    return verts, faces


def read_binvox(file_path):
    file = open(file_path, "rb")
    model = binvox_rw.read_as_3d_array(file)
    volume = model.data
    return volume


def read_npy(file_path, th=0.3):
    volume = np.load(file_path)
    volume = volume.squeeze().__ge__(th)
    return volume


def read_glb(file_path):
    raise Exception("Not implemented!")


def read_ply(file_path):
    raise Exception("Not implemented!")
