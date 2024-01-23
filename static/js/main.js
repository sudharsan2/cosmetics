document.addEventListener("readystatechange",(event) =>{
    if(event.target.readyState==="complete"){
        initApp();
    }
});

const initApp = () =>{
    console.log("ReadyState");

    const URL = "http://127.0.0.1";
    const PORT_NUMBER = ":8000";

    
    const sendBtn = document.getElementById("send-btn")

    sendBtn.addEventListener("click",sendOracleDBErrorCode(URL,PORT_NUMBER));

}
async function sendOracleDBErrorCode(URL, PORT_NUMBER){

    const PATH = "/cos/error_code_response";
    console.log(URL + PORT_NUMBER + PATH);
    // const messageInput = document.getElementById("message-input");
    // let data = {
    //     user_input:"FRM-41082",
    // }
    // const response = await fetch((URL + PORT_NUMBER + PATH),
    //     {
    //         method: METHOD,
    //         headers:{
    //             "Content-Type": "application/json",
    //         },
    //         body:JSON.stringify(data),

    //     }
    // );
    // let result = await response.json();
    // console.log(result); 
}
