let webSocket = null;

function init() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    localStorage.setItem('Authorization', $('#token').val());
}

function connectWebSocket() {
    const token = localStorage.getItem('Authorization') || '';
    if (token) {
        const protocol = window.location.protocol.indexOf('https:') === 0 ? 'wss' : 'ws';
        webSocket = new WebSocket(`${protocol}://${window.location.host}/ws/aichat/test?u_type=1`, token);
        webSocket.onopen = () => managerWebSocket();
        webSocket.onerror = () => {
            console.log('websocket client happened error');
            clearWebSocket();
            setTimeout(connectWebSocket, 3000);
        };
    } else {
        console.log('token is null')
    }
}

function managerWebSocket() {
    if (webSocket) {
        console.log('websocket client is open...');
        webSocket.onmessage = function (event) {
            let response = JSON.parse(event.data);
            console.log(response);
            if ('aichat' === response.sender_type) {
                printAiChatGPTResponse(response.data.content)
            } else {
                printChatGPTResponse(response.data.content)
            }
        };
        // 断开监听
        webSocket.onclose = () => {
            console.log('websocket client has been disconnected, reconnecting...');
            clearWebSocket();
            connectWebSocket();
        };
    } else {
        console.log('websocket client is not open, reconnecting...');
        connectWebSocket();
    }
}

function clearWebSocket() {
    webSocket = null;
}

function printChatGPTResponse(message) {
    let index = 0;
    const responseText = document.getElementById("chatgpt-response");
    responseText.innerHTML = '';
    // 创建一个定时器，每隔一段时间打印一个字符
    const interval = setInterval(function () {
            responseText.innerHTML += message[index];
            index++;
            // 当打印完成时，清除定时器
            if (index >= message.length) {
                scrollToBottom();
                clearInterval(interval);
            }
        },
        50); // 每隔50毫秒打印一个字符
}
function printAiChatGPTResponse(message) {
    let index = 0;
    const responseText = document.getElementById("chatgpt-response");
    responseText.innerHTML += message;
    scrollToBottom();
}

function scrollToBottom() {
    const chatgptResponse = $('#chatgpt-response');
    chatgptResponse.scrollTop(chatgptResponse[0].scrollHeight);
}

$(document).ready(function () {
    init();

    connectWebSocket();

    // submit snippet
    $('#call-chat-server').on('click', function () {
        let user_id = $('#user_id').val();
        const chatGptInput = $('#chat-gpt-input');
        const message = chatGptInput.val();
        if (message.trim() !== '') {
            const data = {action: 'chat', 'user': user_id, data: message};
            webSocket.send(JSON.stringify(data));
            chatGptInput.val('')
            printChatGPTResponse('正在思考，请等待......\n\n')
        }
    })
});

