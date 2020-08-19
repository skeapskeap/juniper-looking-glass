$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
           data : {
               command : $('#command_input').val(),
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
                $('#query_section').text(data.command).show();
                $('#reply_section').html(data.reply).show();
            }
        });
        event.preventDefault();
    });
});