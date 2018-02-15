db.createUser({
    user: "admin",
    pwd: "abc123",
    roles: [{role: dbOwner, db: leanote}]
});
