const cloudinary = require('cloudinary').v2;
const { CloudinaryStorage } = require('multer-storage-cloudinary');

cloudinary.config({
    cloud_name: "YOUR_CLOUD_NAME_HERE",
    api_key: "YOUR_API_KEY_HERE",
    api_secret: "YOUR_API_SECRET_HERE",
});

const storage = new CloudinaryStorage({
    cloudinary,
    params: {
        folder: 'Amenities',
        allowedFormats: ['jpeg', 'png', 'jpg']
    }
});

module.exports = {
    cloudinary,
    storage
}
