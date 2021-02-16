const express = require('express');
const ejsMate = require('ejs-mate');
const path = require('path');

const app = express();

const multer = require('multer');
const { storage } = require('./cloudinary');
const upload = multer({ storage });

app.engine('ejs', ejsMate)
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'))
app.use(express.static(path.join(__dirname, 'public')))

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.render('home')
});

app.listen(3000, () => {
    console.log(`Serving on port 3000`)
})

app.post('/predict', upload.single('image'), (req, res) => {
	
	img = req.file.path

	// code to get prediction
	prediction = ['ur mom', 'The Eiffel Tower', 'MemChu']

	mainPred = prediction[0]
	others = prediction.slice(1)
    res.render('predict', {mainPred, others, img})
});
