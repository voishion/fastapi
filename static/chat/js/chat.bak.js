async function callChatServer() {
    clearChatGPTResponse();

    let problem = $("#chat-gpt-input").val();
    const data = JSON.stringify({
        "messages": [
            {"role": "system", "content": ""},
            {"role": "user", "content": problem},
        ],
        "max_tokens": 2048,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "model": "gpt-3.5-turbo"
    });
    console.log(data);

    const xhr = new XMLHttpRequest();
    const url = "https://api.openai.com/v1/completions";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Authorization", "Bearer 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");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const json = JSON.parse(xhr.responseText);
            const response = json.choices[0].text;
            printChatGPTResponse(response);
        }
    };
    await printChatGPTResponse('正在思考，请等待......');
    await xhr.send(data);
}

function printChatGPTResponse(message) {
    let index = 0;
    const responseText = document.getElementById("chatgpt-response");
    // 创建一个定时器，每隔一段时间打印一个字符
    const interval = setInterval(function () {
            responseText.innerHTML += message[index];
            index++;
            // 当打印完成时，清除定时器
            if (index >= message.length) {
                clearInterval(interval);
            }
        },
        50); // 每隔50毫秒打印一个字符
}

function clearChatGPTResponse() {
    $("#chatgpt-response").text("");
}
function clearChatGPTInput() {
    $("#chat-gpt-input").val("")
}