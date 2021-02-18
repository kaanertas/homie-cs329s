const cloudinary = require('cloudinary').v2;
const { CloudinaryStorage } = require('multer-storage-cloudinary');

cloudinary.config({
    cloud_name: "dlyjr71kx",
    api_key: "833231282457385",
    api_secret: "LEFOthdVyM1Nuyot1fxtAW-xXaw",
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