# 3D Shape Visualizer

There are many libraries to visualize 3D shapes but it's hard to find one to integrate easily to Python code.
This repository supports the most common 3D shape file extensions and do not require complex installation. 

You can use interactive plots to view in 3D or you can save a snapshot of a shape to a png file.
The second usage is particularly useful while dealing with a large 3D shape dataset and requiring an overview of it.
I plan to add more functionality in the future. See the to-do list below.

### To-do

- [ ] Support below file types
  - [x] off, obj, binvox, npy
  - [ ] ply
  - [ ] glb
- [x] Save plots to:
  - [x] png
  - [ ] gif
- [ ] Add args to control the viewpoint
- [ ] Add sample commands to the README
- [ ] Improve requirements.txt

### Long-Term To-do

- [ ] Replace Pytorch3D with [kaleido library](https://github.com/plotly/Kaleido)
- [ ] Draw plots using only kaleido or matplotlib
- [ ] Plot mutliple shapes on top of each other



## References
<a id="1">[1]</a> 
This is how I read binvox files, MANY THANKS to the owner of open-source binvox-rw-py project:

https://github.com/dimatura/binvox-rw-py

<a id="2">[2]</a> 
[Pytorch3D](https://pytorch3d.org) made things really easy :)

Nikhila Ravi, Jeremy Reizenstein, David Novotny, Taylor Gordon, Wan-Yen Lo, Justin Johnson, & Georgia Gkioxari (2020). Accelerating 3D Deep Learning with PyTorch3D. arXiv:2007.08501.

