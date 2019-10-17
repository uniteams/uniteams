function validate(string, pattern) {
  switch (pattern) {
    case "email":
      pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
      break;
    case "password":
      pattern = /^.{8,}$/;
      break;
    case "!empty":
      return (string.length > 0);
    default:
      pattern = /^.+?$/;
  }
  return pattern.test(string) !== false;
}
