const express = require("express");
const { check, validationResult} = require("express-validator");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const router = express.Router();
const auth = require("../middleware/auth");
const fetch = require("node-fetch");

const Property = require("../model/Property");
const User = require("../model/User");

const multer = require('multer');
const { storage } = require('../cloudinary');
const upload = multer({ storage });


/**
 * @method - POST
 * @param - /signup
 * @description - User SignUp
 */

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
      console.log("Inside prop view")
      property = await Property.findOne(property_id)

      res.render('property-view', {property});

  }
)

router.post(

  // TODO

  
    "/create/:userid",
    [
        check("property-name", "Please Enter a Valid Property Name")
        .not()
        .isEmpty(),
        upload.array('image')
    ],

    async (req, res) => {
        const propertyName = req.body['property-name'];

        var img_urls = [];
        req.files.forEach(function(item) {
        img_urls.push(item.path);
        });

    
        const d = {img_urls}

        json = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: JSON.stringify(d),
        headers: { 'Content-Type': 'application/json' }
        }).then(res => res.json())
        .catch(err => console.log(err));

        const {preds,scores,output_urls, preds_consolidated} = json

        property = new Property({
                name: propertyName,
                photo_urls:img_urls,
                labeled_photo_urls:output_urls,
                model_pred_labels: preds_consolidated,
                labels: preds_consolidated,
                });

        await property.save();
        // GET USERNAME
        // PUT PROPERTY IN USER'S LIST
        const {userid} = req.params;
        let user = await User.findOne({_id:userid});
        await user.properties.push(property);
        await user.save();
        console.log(user)
        res.render('property-view', {...json, propertyName});
  }
)

router.post("/:propertyid/update", async (req, res) => {
    console.log("Inside update")
    res.render('property-view', {property});

  }
)

router.post("/:propertyid/update", async (req, res) => {
    console.log("Inside update")
    res.render('property-view', {property});

  }
)

module.exports = router;