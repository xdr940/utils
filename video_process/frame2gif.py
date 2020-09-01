import imageio,os
from path import Path
from tqdm import tqdm
#定义函数,并设置“开始帧”，“结束帧”，“gif的速率”为参数
def saveGif(start_frame,end_frame,gif_speed,folderName,filename):
	#创建frames列表
	frames=[]
	folderName = Path(folderName)
	if folderName.exists()==False:
		print('folder no exist')
		return
	files = folderName.files('*.{}'.format('png'))
	files.sort()
	for img_p in tqdm(files):
		img = imageio.imread(img_p)
		frames.append(img)
	imageio.mimsave(filename, frames, fps=2)  # 利用帧数列表制作gif，设置fps也就是帧速率为参数

	#当i在开始帧到结束帧之间


def main():
	#in_path = '/home/roit/datasets/VisDrone/cc_output/uav0000023_00870_s/'
	#in_path = '/home/roit/datasets/visdrone_raw_256512/uav0000023_00870_s'
	#in_path = '/home/roit/datasets/MC_hv_distr_map/test_hv_basline/test_depth/depths'
	#in_path = '/home/roit/datasets/MC_hv_distr_map/test_hv_basline/concat'
	in_path = './ab'
	in_path = Path(in_path)

	saveGif(start_frame=0, end_frame=10, gif_speed = 5, folderName = in_path, filename = in_path.stem+".gif")
	print('ok')


if __name__=="__main__":
	# print(os.getcwd())
	main()