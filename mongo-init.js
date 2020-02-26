db.users.update(
  { username: "admin" },
  {
    username: "admin",
    password:
      "$6$rounds=656000$X7b.3H5FnxG.H1mZ$onE/9/Nj91AMQx7kGesLBY17LX5my186ggcGg7RNWRZWEuwehAsrckcfD40179NyqtOFe8f5U/Uja98Ji0Be.0",
    project_refs: []
  },
  { upsert: true }
);
