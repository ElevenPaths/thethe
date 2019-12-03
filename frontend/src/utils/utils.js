function object_is_empty(obj) {
  return Object.keys(obj).length === 0 && obj.constructor === Object;
}

function make_unique_list(element_arg, lower = true) {
  let element = element_arg;

  if (element === undefined || element === null) {
    return ["N/D"];
  }

  if (Array.isArray(element)) {
    element = Array.from(new Set(element.map(el => el.toLowerCase())));
  } else {
    if (lower) {
      element = [element.toLowerCase()];
    } else {
      element = [element];
    }
  }
  return element;
}

function from_python_time(python_time) {
  let date = new Date(python_time * 1000);

  return `${date.toLocaleDateString()} at ${date.toLocaleTimeString()}`;
}

export { object_is_empty, make_unique_list, from_python_time };
