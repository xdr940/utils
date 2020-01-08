// 文件名 calc.c
#include <Python.h>
//1. c func
int add(int x, int y){ // C 函数
    return x + y;
}

int sub(int x,int y){
	return x-y;
}

/*
2.
    包裹函数。它负责将Python的参数转化为C的参数（PyArg_ParseTuple）
    调用实际的add_function，并处理add_function的返回值，最终返回给Python环境
*/
static PyObject *calc_add(PyObject *self, PyObject *args){

    int x, y;
    // Python传入参数
    // "ii" 表示传入参数为2个int型参数，将其解析到x, y变量中
    if(!PyArg_ParseTuple(args, "ii", &x, &y))
        return NULL;
    return PyLong_FromLong(add(x, y));
}
static PyObject *calc_sub(PyObject *self, PyObject *args){

    int x, y;
    // Python传入参数
    // "ii" 表示传入参数为2个int型参数，将其解析到x, y变量中
    if(!PyArg_ParseTuple(args, "ii", &x, &y))
        return NULL;
    return PyLong_FromLong(sub(x, y));
}



/*
3. 模块的方法列表,导出表
//它负责告诉Python这个模块里有哪些函数可以被Python调用。
//导出表的名字可以随便起，
//每一项有4个参数：
//第一个参数是提供给Python环境的函数名称，这个名称可以任取，
//第二个参数是包裹函数名字。
//第三个参数的含义是参数变长，
//第四个参数是一个说明性的字符串。
//导出表总是以{NULL,NULL, 0,NULL}结束。
*/
static PyMethodDef CalcMethods[] = {
     {"add", calc_add, METH_VARARGS, "函数描述"},
	 {"sub", calc_sub, METH_VARARGS, "x minux y"},
     {NULL, NULL, 0, NULL}
};




// 模块
static struct PyModuleDef calcmodule = {
    PyModuleDef_HEAD_INIT,
    "calc", // 模块名
    NULL, // 模块文档
    -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
    CalcMethods
};

// 初始化
PyMODINIT_FUNC PyInit_calc(void)
{
/*
导出函数initcpp_module。
这个的名字不是任取的，是你的module名称添加前缀init。
导出函数中将模块名称与导出表进行连接
*/
    return PyModule_Create(&calcmodule);
}



/*
call_tree
PyInit_calc|#PyInit_ModuleName
    |--calcmodule
        |--CalcMethods
            |--calc_add 
				|--add
            |--calc_sub
				|--sub

*/
