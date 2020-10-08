///////////////////////////////////////////////////////////////////////////
//
// Copyright (c) 2001-2011, Industrial Light & Magic, a division of Lucas
// Digital Ltd. LLC
// 
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
// *       Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
// *       Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
// *       Neither the name of Industrial Light & Magic nor the names of
// its contributors may be used to endorse or promote products derived
// from this software without specific prior written permission. 
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
///////////////////////////////////////////////////////////////////////////

//-----------------------------------------------------------------------------
//
//        PyIex -- support for mapping C++ exceptions to Python exceptions
//
//-----------------------------------------------------------------------------


#include "PyIex.h"
#include "PyIexExport.h"
#include <IexErrnoExc.h>

namespace PyIex {

namespace {
static TypeTranslator<IEX_NAMESPACE::BaseExc> *_baseExcTranslator = 0;
}

PYIEX_EXPORT TypeTranslator<IEX_NAMESPACE::BaseExc> &baseExcTranslator()
{
    if (!_baseExcTranslator)
    {
        void *ptr = 0;

        PyObject *mod = PyImport_ImportModule("iex");
        if (mod)
        {
            PyObject *obj = PyObject_GetAttrString(mod, "_baseExcTranslator");
            if (obj)
            {
#if PY_VERSION_HEX < 0x02070000
                if (PyCObject_Check(obj))
                {
                    ptr = PyCObject_AsVoidPtr(obj);
                }
#else
                if (PyCapsule_CheckExact(obj))
                {
                    ptr = PyCapsule_GetPointer(obj, 0);
                }
#endif
                Py_DECREF(obj);
            }
            Py_DECREF(mod);
        }

        if (ptr)
        {
            _baseExcTranslator = (TypeTranslator<IEX_NAMESPACE::BaseExc> *) ptr;
        }
    }
    return *_baseExcTranslator;
}

PYIEX_EXPORT void setBaseExcTranslator(TypeTranslator<IEX_NAMESPACE::BaseExc> *t)
{
    _baseExcTranslator = t;
}

} // namespace PyIex
