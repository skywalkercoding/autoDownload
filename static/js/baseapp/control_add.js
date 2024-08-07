const excelform = document.getElementById('excelAddForm');
const runTaskButton=document.getElementById('start_task');
const stopTaskButton=document.getElementById('stop_task');
const modalBody  = document.getElementById('modalBody');
const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
const cleardata=document.getElementById('clear_data');

let isRunning = false;
excelform.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(excelform);

            const response = await fetch('/uploadcontrol/', {
                method: 'POST',
                body: formData
            });

            const jsonData = await response.json();

            // 显示返回的JSON数据
            if (jsonData.success) {
                const message = jsonData.message;
                  modalBody.textContent = message;
                $('#myModal').modal('show');
            } else {
                const errorMessage = jsonData.message;
                  modalBody.textContent = errorMessage;
                $('#myModal').modal('show');
            }
        });


  function ckAll(){
  var flag = document.getElementById("allChecks").checked;
  var cks = document.getElementsByName("input[]");
  for(var i=0;i<cks.length;i++){
      cks[i].checked=flag;
  }
}


function MultiDel(){
  if(!confirm("确定删除这些吗?")){
      return;
  }
  var cks=document.getElementsByName("input[]");
  var str = "";
  //拼接所有的id
  for(var i=0;i<cks.length;i++){
      if(cks[i].checked){
          str+=cks[i].value+",";
      }
  }
  //去掉字符串未尾的','
  str=str.substring(0, str.length-1);
//  location.href='/clear/?id='+str;
  fetch('/delControl/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                          loadingContainer.style.display = 'none';
                           overlay.style.display = 'none';

                         location.href='/control/';

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });




}


function StartTask(){
      if(!confirm("开启任务")){
      return;
  }
  var cks=document.getElementsByName("input[]");
  var str = "";
  //拼接所有的id
  for(var i=0;i<cks.length;i++){
      if(cks[i].checked){
          str+=cks[i].value+",";
      }
  }
  //去掉字符串未尾的','
  str=str.substring(0, str.length-1);
  fetch('/runTask/?id='+str)
                 .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         runTaskButton.style.display='block';
                          runTaskButton.classList.add('disabled');


                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });
}

function StopTask(){
      if(!confirm("停止任务")){
      return;
  }
  var cks=document.getElementsByName("input[]");
  var str = "";
  //拼接所有的id
  for(var i=0;i<cks.length;i++){
      if(cks[i].checked){
          str+=cks[i].value+",";
      }
  }
  //去掉字符串未尾的','
  str=str.substring(0, str.length-1);
  fetch('/stopTask/?id='+str)
                 .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         runTaskButton.style.display='block';
                          runTaskButton.classList.remove('disabled');



                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });
}

