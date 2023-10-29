$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function getUa() {
        let userAgentStr = navigator.userAgent
        const userAgentObj = {
            browserName: '',    // 浏览器名称
            browserVersion: '', // 浏览器版本
            osName: '',         // 操作系统名称
            osVersion: '',      // 操作系统版本
            deviceName: '',     // 设备名称
        }

        for (let key in browserReg) {
            if (browserReg[key].test(userAgentStr)) {
                userAgentObj.browserName = key
                if (key === 'Chrome') {
                    userAgentObj.browserVersion = userAgentStr.split('Chrome/')[1].split(' ')[0]
                } else if (key === 'IE') {
                    userAgentObj.browserVersion = userAgentStr.split('MSIE ')[1].split(' ')[1]
                } else if (key === 'Firefox') {
                    userAgentObj.browserVersion = userAgentStr.split('Firefox/')[1]
                } else if (key === 'Opera') {
                    userAgentObj.browserVersion = userAgentStr.split('Version/')[1]
                } else if (key === 'Safari') {
                    userAgentObj.browserVersion = userAgentStr.split('Version/')[1].split(' ')[0]
                } else if (key === '360') {
                    userAgentObj.browserVersion = ''
                } else if (key === 'QQBrowswe') {
                    userAgentObj.browserVersion = userAgentStr.split('Version/')[1].split(' ')[0]
                }
            }
        }

        for (let key in deviceReg) {
            if (deviceReg[key].test(userAgentStr)) {
                userAgentObj.osName = key
                if (key === 'Windows') {
                    userAgentObj.osVersion = userAgentStr.split('Windows NT ')[1].split(';')[0]
                } else if (key === 'Mac') {
                    userAgentObj.osVersion = userAgentStr.split('Mac OS X ')[1].split(')')[0]
                } else if (key === 'iPhone') {
                    userAgentObj.osVersion = userAgentStr.split('iPhone OS ')[1].split(' ')[0]
                } else if (key === 'iPad') {
                    userAgentObj.osVersion = userAgentStr.split('iPad; CPU OS ')[1].split(' ')[0]
                } else if (key === 'Android') {
                    userAgentObj.osVersion = userAgentStr.split('Android ')[1].split(';')[0]
                    userAgentObj.deviceName = userAgentStr.split('(Linux; Android ')[1].split('; ')[1].split(' Build')[0]
                }
            }

        }
        return userAgentObj
    }

    let user_id = "325489464903640";
    const protocol = window.location.protocol.indexOf('https:') === 0 ? 'wss' : 'ws';
    const webSocket = new WebSocket(
        `${protocol}://${window.location.host}/ws/aichat/test?u_id=${user_id}`
    );

    // 连接建立后的回调函数
    webSocket.onopen = function () {
        console.log("已经建立websocket连接")
    }

    // 接收到服务器消息后的回调函数
    webSocket.onmessage = function (event) {
        const received_msg = event.data;
        console.log(received_msg)
    }
    // 连接关闭后的回调函数
    webSocket.onclose = function () {
        // 关闭 websocket
        console.log("连接已关闭...");
    }

    // submit snippet
    $('#call-chat-server').on('click', function () {
        console.log("xsaxsaxsa")
        const $snippet_textarea = $('#chat-gpt-input');
        const message = $snippet_textarea.val();
        if (message.trim() !== '') {
            webSocket.send(message);
            $snippet_textarea.val('')
        }
    })
})

