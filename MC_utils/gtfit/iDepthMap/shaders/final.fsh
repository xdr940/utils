#version 120

float BLUR_AMOUNT = 1.6; //I preffere something between 1.0 and 2.0
#define clipping far//48*16 = 768

//https://github.com/sp614x/optifine/blob/master/OptiFineDoc/doc/shaders.txt
uniform sampler2D depthtex0;
uniform sampler2D shadowtex0;
uniform sampler2D  gdepthtex;
uniform sampler2D composite;
uniform sampler2D noisetex;
/*
depthtex0   everything
depthtex1   no translucent objects (water, stained glass)
depthtex2   no translucent objects (water, stained glass), no handheld objects
*/
uniform float near;// near viewing plane distance,全黑，等于0.05
uniform float far;// far viewing plane distance ,全白, 等于设置里的renders distances, 768
uniform sampler2D normals;
varying vec4 texcoord;//varying 存储的是顶点着色器的输出，同时作为片段着色器的输入

vec4 getDepth(vec2 coord) {
  /*
  返回值在0.~1.之间
  0 = 白色,255灰度， 1= 黑色0灰度
  return 1-temp, 天黑色， 近处比较灰色

  */
  //float far = 512;
  vec4 temp = texture2D(depthtex0, coord);

//1. origin
return  2.0 * near * far / (far + near - (2.0 * temp - 1.0) * (far - near)) / clipping;
//760,181
//700 171
//650 162
//600 152
//550 142
//500 132
//450 121
//400 110
//350 99
//300 86
//250 74
//200 60
//190 58
//180 55
//170 52
//160 49
//150 46
//140 43
//130 41
//120 38
//110 35
//100 32
//90 29
//80 26
//70 23
//60,19
//50 16
//40,13
//30,10
//20 7
//10 3
//5 2
//0,0



//2
//return  2.5 * near * far / (far + near - (2.0 * temp - 1.0) * (far - near)) / clipping;
//200,75
//300,108
//400,138
//500,165
//600,190
  //700,213
  //750,225
  // 760,227,
  // 766,255
  //768,255
  // 767,255
  // 770,255

//3
  //float f=800.0;
  // return  2.5 * near * f / (f + near - (2.0 * temp - 1.0) * (f - near)) / clipping;
//700,219
// 600,195
//500,169
// 400,140
// 300,109

//4
  //return  3.0 * near * far / (far + near - (2.0 * temp - 1.0) * (far - near)) / clipping;
//100,48
//200,90
//300,129
//400,165
//500,198
//600,228
//700,255

//return (1/(1-temp))/10000;//优化有用
//300,201
// 400,255
  //return far/768-temp;
  //return (1/(1-temp))/20000;//优化有用
//400,149  700,255  600,255灰度
//  return (1/(1-temp))/30000;//优化有用
//600,193
//700,255
  //
//   return (1/(1-temp))/35000;//优化有用
//700,227
//

  //return 1- (1-temp)*10000;
  //return 1.0-temp;//全黑
  //return temp;//天白色， 近处灰色
  //return 1000*temp;//全白色
  //return 10000*temp;// all white like last
  //return 1000-1000*temp;//50m以内全白色
  //return 500-500*temp;//30m处以内全白色


  //return 100*(1-temp);//5m内全白色， 但是远处很快就黑色了,50m中心灰度24
  //5,233   delta x 233 = 0.91015625 = f(temp), temp = 0.990898437
  //10,121, 3.90625e-3 x 121 = 0.47265625 = f(temp), temp = 0.995273437
  //20,61  delta x 61 =0.23828125 = f(temp), temp = 0.997617187
  //50,24
  //100,12
  //200,5
  //300,3
  //400,2
  //500,1

//  return (temp-0.99)*100;
//200,250
//300,252
//



  //return 1- 100*(1-temp);//50m center 231,100mcenter 243
  //return 10-10*temp;//
  //return 51-50*temp;//全白色，理所当然
//return 50-50*(temp);
  //
  //远处太暗， 近处太亮, 50m 中心灰度 12，100m中心灰度6，6,6；200m center 3,3,3,  300m中心灰度 2,2,2


//  return normalize(temp);
  //texture2D(depthtex0,coord) ->0.999非常接近，原因以及如何操作

  //return texture2D(depthtex0,coord)/far*2;
  //return texture2D(normals,coord);
  //return vec4(near,near,near,1);
  //return 0;//全黑
	//return 1;//全白
	//return 0.5;//全灰色

}
//texture2D
/*
The texture2D function returns a texel, i.e. the (color) value of the texture for the given coordinates.
 The function has one input parameter of the type sampler2D and one input parameter of the type vec2 : sampler,
  the uniform the texture is bound to, and coord, the 2-dimensional coordinates of the texel to look up.

There are texture lookup functions to access the image data.
Texture lookup functions can be called in the vertex and fragment shader.
 When looking up a texture in the vertex shader, level of detail is not yet computed, however there are some special lookup functions for that (function names end with "Lod").
The parameter "bias" is only available in the fragment shader It is an optional parameter you can use to add to the current level of detail.
Function names ending with "Proj" are the projective versions, the texture coordinate is divided by the last component of the texture coordinate vector.

*/


void main() {
	vec4 depth = getDepth(texcoord.st);

  //关于texcoord.st : 就是前两位分量， 由于这个四维向量代表的是纹理， 为了代码可解释性
  //就用.st索引， 用xy索引其实一样，就是为了更方便理解，如下
  /*
  if (depth.z>0.5){
    gl_FragColor = vec4(1, 0,0, 1.0);
  }else{
    gl_FragColor = vec4(0,1,0, 1.0);


  }
*/
  /*
  You may also wonder why "rgba" is used and not "xyzw".
  GLSL allows using the following names for vector component lookup:
x,y,z,w	Useful for points, vectors, normals
r,g,b,a	Useful for colors
s,t,p,q	Useful for texture coordinates

  */
	gl_FragColor = vec4(depth.xyz, 1.0);

}
