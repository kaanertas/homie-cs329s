const express = require('express');
const ejsMate = require('ejs-mate');
const path = require('path');
const fetch = require('node-fetch');
const bodyParser = require("body-parser");
require("./model/Property");
require("./model/User");
const property = require("./routes/property");
const user = require("./routes/user");
const InitiateMongoServer = require("./config/db");

InitiateMongoServer();

const app = express();

const port = process.env.PORT || 3000;

const multer = require('multer');
const { storage } = require('./cloudinary');
const upload = multer({ storage });

app.engine('ejs', ejsMate)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'))
app.use(express.static(path.join(__dirname, 'public')))

app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.render('home')
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Serving on port ${port}`)
})

app.use("/user", user);
app.use("/property", property);

