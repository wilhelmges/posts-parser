// Load sql.js WebAssembly file
let config = {
    locateFile: () => "sql-wasm.wasm",
};
const dbfile = 'strapi-dashboard/.tmp/data.db';
initSqlJs(config).then(function (SQL) {
    fetch(dbfile)
        .then(response => response.arrayBuffer())
        .then(buffer => {
            const uint8Array = new Uint8Array(buffer);
            const db = new SQL.Database(uint8Array);
            // Now you can use the db variable to run queries on your database
            console.log("db is opened 🎉");

            db.run(("INSERT INTO categories(title) VALUES (?)"), ['games'])

            const categories = db.exec("SELECT * FROM categories");
            console.log(categories);

            const data = db.export();
            let buffer2 = new Buffer(data);
            fs.writeFileSync(dbfile, buffer2);
        })
        .catch(console.error);
    console.log("sql.js initialized");
});