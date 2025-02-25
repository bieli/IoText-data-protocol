// This check is new and seems buggy (possibly with PyO3 interaction)
#![allow(clippy::borrow_deref_ref)]

extern crate pyo3;

use std::collections::{HashSet, hash_map, HashMap};

use iotext_rs::IoTextDataRow;
// use iotext_rs::IoTextData;
// use iotext_rs::IoTextDataRow;
use pyo3::PyResult;
use pyo3::exceptions::PyTypeError;
// use pyo3::PyErr;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple, IntoPyDict};
use pyo3::wrap_pyfunction;
use rayon::prelude::*;


#[pyfunction]
fn length(py: Python, obj: PyObject) -> PyResult<PyObject> {
    if let Ok(s) = obj.extract::<String>(py) {
        return Ok(s.len().to_object(py));
    }
    if let Ok(s) = obj.extract::<Vec<String>>(py) {
        return Ok(s.len().to_object(py));
    }
    Err(PyTypeError::new_err("Not Supported"))
}


/// Searches for the word, parallelized by rayon
#[pyfunction]
fn search(contents: &str, needle: &str) -> usize {
    contents
        .par_lines()
        .map(|line| count_line(line, needle))
        .sum()
}

#[pyfunction]
fn decode(py: Python, obj: PyObject) -> PyResult<PyObject> {
    if let Ok(s) = obj.extract::<String>(py) {
        return Ok(s.len().to_object(py));
    }
    Err(PyTypeError::new_err("Not Supported"))
//    let data_obj: IoTextDataRow = IoTextDataRow::default();
//    return PyObject(data_obj.parse_iotext_str(iot_ext_data_row)).into_py()
}

//#[pyfunction]
//fn decode() -> PyResult<IoTextDataRow> {
//   Ok(IoTextDataRow::default())
//}

//#[pyfunction]
//fn decode2() -> PyResult<Py<IoTextDataRow>> {
//    // let gil = Python::acquire_gil();
//    // let py = gil.python();
//
//    Py::new(py, IoTextDataRow::default()).into()
//}

#[pyclass]
struct Nonzero {
    value: i32,
}

//#[pymethods]
//impl Nonzero {
//    #[new]
//    fn py_new(value: i32) -> PyResult<Self> {
//        if value == 0 {
//            Err(PyErr::new("cannot be zero"))
//        } else {
//            Ok(Nonzero { value: value })
//        }
//    }
//}

#[pyclass]
struct MyClass {
    num: i32,
}

#[pyfunction]
fn return_myclass() -> Py<MyClass> {
    Python::with_gil(|py| Py::new(py, MyClass { num: 1 }).unwrap())
}


#[pyclass]
#[derive(Default)]
struct MyIoTextClass {
    value: IoTextDataRow,
}

#[pymethods]
impl MyIoTextClass {
    #[new]
    fn new() -> Self {
        MyIoTextClass { value: IoTextDataRow::default() }
    }

    pub fn example_list(&mut self, py: Python) -> PyResult<PyObject> {
        //let l: &PyList = PyList::empty(py);
        let elements: Vec<&str> = vec!["a", "b", "c"];
        let l: &PyList = PyList::new(py, elements);
        Ok(l.into())
    }

    //pub fn example_dict_1(&mut self, py: Python) -> PyResult<PyDict> {
        //let l: &PyList = PyList::empty(py);
        //let elements: HashMap<&str, &str> = (0..10).map(|i| (i.to_string(), i.to_string())).collect();
        //let l: &PyDict = PyDict::new(py);
    //    let key_vals: Vec<(&str, PyObject)> = vec![
    //        ("num", 8.to_object(py)), ("str", "asd".to_object(py))
    //    ];
        //let dict = key_vals.into_py_dict(py);

    //    Ok(key_vals.into_py_dict(py))
    //}

    /// Formats the sum of two numbers as string.
    pub fn get_result(&mut self, py: Python) -> PyResult<HashMap<String, String>> {
        let mut result = HashMap::new();
        result.insert("name".to_string(), "kushal".to_string());
        result.insert("age".to_string(), "36".to_string());
        Ok(result)
    }


    //fn method1() -> PyResult<&PyDict> {
    //}

    //#[getter]
    //fn value(&self) -> PyResult<IoTextDataRow> {
    //    Ok(self.value)
    //}
}

#[pyfunction]
fn return_myiotextclass() -> Py<MyIoTextClass> {
    Python::with_gil(|py| Py::new(py, MyIoTextClass { value: IoTextDataRow::default() }).unwrap())
}






/// Count the occurrences of needle in line, case insensitive
fn count_line(line: &str, needle: &str) -> usize {
    let mut total = 0;
    for word in line.split(' ') {
        if word == needle {
            total += 1;
        }
    }
    total
}

#[pyfunction]
// Returns a Person class, takes a dict with {"name": "age", "age": 100} format.
fn give_me_a_person(data: &PyDict) -> PyResult<Person> {
    let name: String = data.get_item("name").unwrap().extract().unwrap();
    let age: i64 = data.get_item("age").unwrap().extract().unwrap();

    let p: Person = Person::new(name, age);
    Ok(p)
}

#[pyclass]
#[derive(Debug)]
struct Person {
    #[pyo3(get, set)]
    name: String,
    #[pyo3(get, set)]
    age: i64,
}

#[pymethods]
impl Person {
    #[new]
    fn new(name: String, age: i64) -> Self {
        Person { name, age }
    }
}

#[pymodule]
fn iotext(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search, m)?)?;
    m.add_function(wrap_pyfunction!(return_myclass, m)?)?;
    m.add_class::<MyClass>()?;
    m.add_function(wrap_pyfunction!(return_myiotextclass, m)?)?;
    m.add_class::<MyIoTextClass>()?;
    m.add_wrapped(wrap_pyfunction!(length))?;
    m.add_wrapped(wrap_pyfunction!(decode))?;
    m.add_wrapped(wrap_pyfunction!(give_me_a_person))?;
    m.add_class::<Person>()?;

    Ok(())
}