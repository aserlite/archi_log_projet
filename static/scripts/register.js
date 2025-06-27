document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('profile_picture_input');
    const output = document.getElementById('profile_picture_base64');

    input.addEventListener('change', function () {
        const file = this.files[0];
        if (!file || !file.type.startsWith('image/')) return;

        const img = new Image();
        const reader = new FileReader();

        reader.onload = function (e) {
            img.src = e.target.result;
        };

        img.onload = function () {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            let quality = 0.95;
            let base64 = "";
            do {
                base64 = canvas.toDataURL('image/jpeg', quality);
                quality -= 0.05;
            } while (base64.length > 1_048_576 && quality > 0.1);

            output.value = base64;
            console.log('Compressed base64 size:', (base64.length / 1024).toFixed(1), 'KB');
        };

        reader.readAsDataURL(file);
    });
});
