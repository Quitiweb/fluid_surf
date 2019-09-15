/**
 * Created by grego on 5/09/19.
 */
(function ($) {
    var doc = new jsPDF();

    var elementHandler = {
        '#ignorePDF': function (element, renderer) {
            return true;
        }
    };


    $('#print-to-pdf').click(function () {
        print();
    });


// Variant
// This one lets you improve the PDF sharpness by scaling up the HTML node tree to render as an image before getting pasted on the PDF.
    function print(quality = 2) {
        const filename = 'QRlist.pdf';

        html2canvas(document.querySelector('#qr-list')
        ).then(canvas => {
            let pdf = new jsPDF('p', 'mm', 'a4');

            pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 211, 300);
            pdf.save(filename);
        });
    }

    


})(jQuery);
