/**
 * Created by grego on 3/09/19.
 */
(function ($) {
    //Variables para detectar y dibujar donde se detecta el qr
    var video = document.createElement("video");
    var canvasElement = document.getElementById("canvas");
    var canvas = canvasElement.getContext("2d");
    var loadingMessage = document.getElementById("loadingMessage");
    var outputContainer = document.getElementById("output");
    var outputMessage = document.getElementById("outputMessage");


    //Dibuja la línea que rodea el QR
    function drawLine(begin, end, color) {
        canvas.beginPath();
        canvas.moveTo(begin.x, begin.y);
        canvas.lineTo(end.x, end.y);
        canvas.lineWidth = 4;
        canvas.strokeStyle = color;
        canvas.stroke();
    }

    //Detecta la webcam o la cámara del móvil
    // Use facingMode: environment to attemt to get the front camera on phones
    navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}}).then(function (stream) {
        video.srcObject = stream;
        video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
        video.play();
        requestAnimationFrame(tick);
    });

    //Funcion que se ejecuta cada frame
    function tick() {
        loadingMessage.innerText = "⌛ Loading video..."
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            loadingMessage.hidden = true;
            canvasElement.hidden = false;
            outputContainer.hidden = false;

            canvasElement.height = video.videoHeight;
            canvasElement.width = video.videoWidth;
            canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
            var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
            var code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts: "dontInvert",
            });
            if (code) {
                drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#7629EF");
                drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#7629EF");
                drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#7629EF");
                drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#7629EF");
                outputMessage.hidden = true;
                lauchUrl(code.data)
            } else {
                outputMessage.hidden = false;

            }
        }
        requestAnimationFrame(tick);
    }

    //Funcion para que cuando detecte un qr, compruebe si es válido (parsea el json y obtiene los campos) y si es válido, redirige a la página web
    function lauchUrl(content) {
        $('#autoform').attr("action", "articulo-detail/");
        console.log(content);

        var json = JSON.parse(content);

        var pdv = json['pdv'];
        var id = json['id'];
        var tipo = json['tipo'];
        if (tipo == 'articulo') {
            $('#autoform').attr("action", "/articulo-detail/" + pdv + "/" + id);
            $('#autoform').submit();
        }
    }
})(jQuery);