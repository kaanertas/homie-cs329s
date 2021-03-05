const express = require('express');
const ejsMate = require('ejs-mate');
const path = require('path');
const fetch = require('node-fetch');

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

app.post('/predict', upload.array('image'), async (req, res) => {
	
	var img_urls = [];
	req.files.forEach(function(item) {
	    img_urls.push(item.path);
	});

	var roomLabel = "room"
	if (req.body.room) roomLabel = req.body.room;
	// const no_preds = req.body.no_preds
	const b = {img_urls}
	
	json = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    body: JSON.stringify(b),
    headers: { 'Content-Type': 'application/json' }
	}).then(res => res.json())
  	.catch(err => console.log(err));

  	res.render('predict', {...json, roomLabel});
    
});
