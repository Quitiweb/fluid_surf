/**
 * Created by grego on 9/09/19.
 */
$(function () {
    var action;

    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) { //Detecta si estoy en un movil o en navegador pc
        $(".number-spinner button").bind("touchstart", (function () {
            btn = $(this);
            input = btn.closest('.number-spinner').find('input');
            btn.closest('.number-spinner').find('button').prop("disabled", false);
            if (btn.attr('data-dir') == 'up') {
                action = setInterval(function () {
                    if (input.attr('max') == undefined || parseInt(input.val()) < parseInt(input.attr('max'))) {
                        input.val(parseInt(input.val()) + 1);
                    } else {

                        btn.prop("disabled", true);
                        clearInterval(action);
                    }
                }, 100);
            } else {
                action = setInterval(function () {
                    if (input.attr('min') == undefined || parseInt(input.val()) > parseInt(input.attr('min'))) {
                        input.val(parseInt(input.val()) - 1);
                    } else {
                        btn.prop("disabled", true);
                        clearInterval(action);
                    }
                }, 100);
            }
        })).bind("touchend", (function () {
            clearInterval(action);
            input.trigger("change");
        }));

        $(".number-spinner button").click(function () {
            btn = $(this);
            input = btn.closest('.number-spinner').find('input');
            btn.closest('.number-spinner').find('button').prop("disabled", false);
            if (btn.attr('data-dir') == 'up') {
                if (input.attr('max') == undefined || parseInt(input.val()) < parseInt(input.attr('max'))) {
                    input.val(parseInt(input.val()) + 1);
                }
            } else {
                if (input.attr('min') == undefined || parseInt(input.val()) > parseInt(input.attr('min'))) {
                    input.val(parseInt(input.val()) - 1);
                }
            }
            input.trigger("change");
        });
    } else {
        $(".number-spinner button").mousedown(function () {
            btn = $(this);
            input = btn.closest('.number-spinner').find('input');
            btn.closest('.number-spinner').find('button').prop("disabled", false);

            if (btn.attr('data-dir') == 'up') {
                action = setInterval(function () {
                    if (input.attr('max') == undefined || parseInt(input.val()) < parseInt(input.attr('max'))) {
                        input.val(parseInt(input.val()) + 1);
                    } else {
                        btn.prop("disabled", true);
                        clearInterval(action);
                    }
                }, 50);
            } else {
                action = setInterval(function () {
                    if (input.attr('min') == undefined || parseInt(input.val()) > parseInt(input.attr('min'))) {
                        input.val(parseInt(input.val()) - 1);
                    } else {
                        btn.prop("disabled", true);
                        clearInterval(action);
                    }
                }, 50);
            }
        }).mouseup(function () {
            clearInterval(action);
            input.change();
        });
    }

});