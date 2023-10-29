$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    // /**
    //  * 客户端接收服务器端消息
    //  */
    // socket.on('answer', function (data) {
    //     console.log(data)
    // });

    // submit snippet
    $('#call-chat-server').on('click', function () {
        console.log("xsaxsaxsa")
        var $snippet_textarea = $('#chat-gpt-input');
        var message = $snippet_textarea.val();
        if (message.trim() !== '') {
            socket.emit('question', {'message':message});
            $snippet_textarea.val('')
        }
    });

});

    /**
     * 客户端接收服务器端消息
     */
    socket.on('answer', function (data) {
        console.log(data)
    });
