# 学习

### 文献
 1. A Survey on Deep Learning Architectures for Image-based Depth Reconstruction.pdf
综述,参考文献基本概括这个方向所有需要看的文章

 2. Depth Map Prediction from a Single Image using a Multi-Scale Deep Network.pdf
首次通过深度学习来解决深度估计任务,单目有监督

 3. Unsupervised Learning of Depth and Ego-Motion from Video.pdf
首次通过无监督,多任务学习解决深度估计任务,2017CVPR oral, 被引量400+,有pytorch代码

 4. Competitive Collaboration- Joint Unsupervised Learning of Depth, Camera.pdf
上篇文章的增强版,2019cvpr poster

 5. Depth from Videos in the Wild- Unsupervised Monocular Depth Learning from Unknown Cameras.pdf
测试数据集和项目比较贴近,2019 ICCV poster

6. Digging into Self-Supervised Monocular Depth Prediction (ICCV 2019 poster)
效果好, 网络小, 主要看

### 资料

 - google学术,翻不了墙用[镜像](http://ac.scmor.com/)
 - 预印本[arxiv](https://arxiv.org/search/?query=&searchtype=title&abstracts=hide&order=-announced_date_first&size=50)
 - 知乎,csdn搜索 深度估计
 - 文献被引说明可以找这个[网站](https://www.semanticscholar.org/)
 - 中国计算机学会（CCF）推荐国际学术会议和期刊目录：[网站](https://www.ccf.org.cn/xspj/gyml/)
 因为计算机视觉更新较快, 中文文章不用看太多

### 代码

建议看pytorch的,易懂,重点看文献3,6代码

 - 文献3 [tensorflow]( https://github.com/tinghuiz/SfMLearner)
 - 文献3 [pytorch]( https://github.com/ClementPinard/SfmLearner-Pytorch )
 - 文献4 [pytorch](https://github.com/anuragranj/cc)
 - 文献6 [pytorch](https://github.com/nianticlabs/monodepth2)

### 用到的数据集

 - [kitti自动驾驶](http://www.cvlibs.net/datasets/kitti/eval_scene_flow.php?benchmark=stereo)

    有光流，摄像机位姿，深度的ground-truth

 - [visdrone](http://www.aiskyeye.com/)

    识别,检测,跟踪等任务用到的无人机航拍数据集, 没有深度的ground-truth

 - [Minecraft](https://github.com/xdr940/Minecraft_tools) 

 这个自己做的,有深度和面法向(surface normal),摄像机位姿的ground-truth,可以用来训练和评估模型

### 工具

- 语言：python
- 文献管理工具： Mendeley
- pdf阅读器 ：
- 论文写作：Latex
- 深度学习框架 Pytorch

# 工作任务

1. 做数据集，主要是GLSL编程， 已经实现了(我没搞清楚原理)
2. 深度学习骨干网络的（主要是FCN，UNET）原理学习和改进
3. 框架改良，从自动驾驶的背景弄到航拍
4. CUDA编程，因为有个函数pytorch没有
