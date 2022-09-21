#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <netinet/ip.h>
#include <sys/types.h>
#include <sys/socket.h>

static PyObject *real_setsockopt(PyObject *self, PyObject *args)
{
    int ret;
    int fd, tos;

    if (!PyArg_ParseTuple(args, "ii", &fd, &tos))
    {
        return NULL;
    }

    ret = setsockopt(fd, IPPROTO_IP, IP_TOS, &tos, sizeof(tos));
    
    return Py_BuildValue("i", ret);
}

static PyMethodDef ExportMethods[] = {
    {"setsockopt", real_setsockopt, METH_VARARGS, "real setsockopt."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef export =
{
    PyModuleDef_HEAD_INIT,
    "sock_ext",   /* name of module */
    "",             /* module documentation, may be NULL */
    -1,             /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    ExportMethods
};

PyMODINIT_FUNC PyInit_sock_ext(void)
{
    return PyModule_Create(&export);
}
