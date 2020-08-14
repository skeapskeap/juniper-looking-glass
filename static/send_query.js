$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
           data : {
               message : $('#query_input').val(),
               target : $('#target_input').val()
           },
           type : 'POST',
           url : '/query'
        })
        .done(function(data) {
            if (data.error) {
                $('#query_section').html(data.error).show();
                $('#reply_section').hide();
            }
            else {
                $('#reply_section').html(data.reply).show();
                $('#query_section').text(data.message).show();
            }
        });
        event.preventDefault();
    });
});