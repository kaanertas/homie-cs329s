const express = require("express");
const { check, validationResult} = require("express-validator");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const router = express.Router();
const auth = require("../middleware/auth");
const fetch = require("node-fetch");

const Property = require("../model/Property");
const User = require("../model/User");
const Misclassified = require("../model/Misclassified");
const classes = require("../public/classes")

const multer = require('multer');
const { storage } = require('../cloudinary');
const upload = multer({ storage });



 router.get('/new/:userid', async (req, res) => {

  const {userid} = req.params;
    try {
      let user = await User.findOne({_id:userid});
      if (!user)
        return res.status(400).json({
          message: "User Not Exist"
        });
      res.render('property-new',{user})
    } catch (e) {
      console.error(e);
      res.status(500).json({
        message: "Server Error"
      });
    }
  
 })

 router.get("/:propertyid/view", async (req, res) => {
    // get property id from url
    const property_id = req.params.propertyid
    try {
        let property = await Property.findOne({_id:property_id}).populate('user')
        // let user = await User.findOne( { 'properties': property_id } );
        let user = property.user
        if (!user)
            return res.status(400).json({ message: "User Not Exist"});
        res.render('property-view', {property, user, classes});
    } catch (e) {
        console.error(e);
        res.status(500).json({ message: "Server Error"});
    }
})

router.post(
    "/create/:userid",
    [
        check("property-name", "Please Enter a Valid Property Name")
        .not()
        .isEmpty(),
        upload.array('image')
    ],

    async (req, res) => {

        const {userid} = req.params;
        const user_id = userid
        let user = await User.findOne({_id:userid});
        if (!user)
          return res.status(400).json({
            message: "User Not Exist"
        });
        const propertyName = req.body['property-name'];

        var img_urls = [];
        req.files.forEach(function(item) {
        img_urls.push(item.path);
        });

        const d = {img_urls}

        json = await fetch('http://0.0.0.0:5000/predict', {
        method: 'POST',
        body: JSON.stringify(d),
        headers: { 'Content-Type': 'application/json' }
        }).then(res => res.json())
        .catch(err => console.log(err));

        const {preds,scores,output_urls, preds_consolidated} = json

        property = new Property({
                name: propertyName,
                user: user,
                photo_urls:img_urls,
                labeled_photo_urls:output_urls,
                model_pred_labels: preds_consolidated,
                labels: preds_consolidated,
                });

        await property.save();
        await user.properties.push(property);
        await user.save();
        res.redirect('/property/'+property._id+'/view');
  }
)

router.post("/:propertyid/update", async (req, res) => {
    
    property_id = req.params.propertyid

    let property = await Property.findOne({_id:property_id});
        if (!property)
          return res.status(400).json({
            message: "User Not Exist"
        });

    model_pred_labels = property.model_pred_labels
    updated_labels = []
    false_pos = []
    false_neg = []
    for (let i=0; i<classes.length; i++) {
        if (req.body['class_'+i]) {
            updated_labels.push(classes[i])
            if (!model_pred_labels.includes(classes[i])) {
                false_neg.push(classes[i])
            }
        }
        else if (model_pred_labels.includes(classes[i])) {
            false_pos.push(classes[i])
        }
    }
    console.log(false_pos)
    console.log(false_neg)

    property.labels = updated_labels;
    await property.save();

    misclassified = new Misclassified({
                false_positives: false_pos,
                flase_negatives: false_neg,
                property: property,
                });
    await misclassified.save();

    res.redirect('/property/'+property_id+'/view')

  }
)


module.exports = router;