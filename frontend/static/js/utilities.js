const API = 'http://localhost:8080/api/v1'

function validate(string, pattern) {
  pattern = /^.+?$/;
  switch (pattern) {
    case "email":
      pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
      break;
    case "password":
      pattern = /^.{8,}$/;
      break;
    case "!empty":
      return (string.length > 0);
  }

  return pattern.test(string) !== false;
}
