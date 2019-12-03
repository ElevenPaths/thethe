const string_to_decimal = ip => {
  let ip_to_convert = ip.split(".").map(bloq => Number.parseInt(bloq));
  return (
    (ip_to_convert[0] << 24) +
    (ip_to_convert[1] << 16) +
    (ip_to_convert[2] << 8) +
    ip_to_convert[3]
  );
};

const compare_ip_addreses = (a, b) => {
  if (
    string_to_decimal(a.canonical_name) > string_to_decimal(b.canonical_name)
  ) {
    return 1;
  } else if (
    string_to_decimal(a.canonical_name) < string_to_decimal(b.canonical_name)
  ) {
    return -1;
  } else {
    return 0;
  }
};

export default compare_ip_addreses;
