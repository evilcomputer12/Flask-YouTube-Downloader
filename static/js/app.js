$(document).ready(function () {
    $('button[type="submit"]').attr('disabled', true);
    $('input[type="text"]').on('keyup', function () {
        var text_value = $('input[name="link"]').val();
        var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
        var p1 = /^.*(youtu.be\/|list=)([^#\&\?]*).*/;
        if (text_value.match(p) || text_value.match(p1)) {
            $('button[type="submit"]').attr('disabled', false);
            $("#input_error").hide();
            validateYouTubeUrl();

        }
        else {
            $('button[type="submit"]').attr('disabled', true);
            $("#input_error").show();
        }
    });
    function validateYouTubeUrl() {
        var url = $('#link').val();
        if (url != undefined || url != '') {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
            var match = url.match(regExp);
            var p1 = /^.*(youtu.be\/|list=)([^#\&\?]*).*/;
            var match1 = url.match(p1);
            if (match || match1) {
                // Do anything for being valid
                // if need to change the url to embed url then use below line
                $('#videoObject').attr('src', 'https://www.youtube.com/embed/' + match[2] + '?autoplay=1&enablejsapi=1');
            } else {
                alert('not valid');
                // Do anything for not being valid
            }
        }
    }

    $('form').on('submit', function(event) {
        $('#kopce').replaceWith("<button type='submit' class='btn btn-primary btn-lg btn-block' id='kopce'disabled><i class='fa fa-refresh fa-spin'></i>Downloading...</button>");
        $('#name').text('');

        $.ajax({
            data : {
                link : $('#link').val()
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data) {
                event.preventDefault();
                var urlname = data.download;
                $('#kopce').replaceWith("<button type='submit' class='btn btn-primary btn-lg btn-block' id='kopce'>Download</button>");
                window.location.replace("/download/"+urlname);
        });
        event.preventDefault();

    });

  });
