const excelform = document.getElementById('excelAddForm');
const showPopupButton = document.getElementById('nextButton');
const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
const cleardata=document.getElementById('clear_data')

//点击next跳到下一步，进行loading加载
let isRunning = false;
let loadingText = "CheckVersion";
let loadingDots = "";
const maxDots = 3; // 最多显示的点个数
showPopupButton.addEventListener('click', function() {
            isRunning = !isRunning;
            if (isRunning){
                showPopupButton.classList.add('disabled');
                 showPopupButton.textContent = 'Stop';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

             fetch('/loading/')  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                        loadingText = "CheckVersion";
                         loadingDots = "";
                       window.location.href = '/check/';  // 跳转到目标页面
                    }else{
                     showPopupButton.classList.remove('disabled');
                     showPopupButton.textContent = 'Run';
                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     loadingText = "CheckVersion";
                     loadingDots = "";
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });

            }

 });



//Upload Excel 各种弹窗展示
const modalBody  = document.getElementById('modalBody');
modalBody.addEventListener("click", function() {
    $('#myModal').modal('hide'); // 关闭模态框
    window.location.href = "/"; // 替换为实际的页面URL
});
excelform.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(excelform);

            const response = await fetch('/upload/', {
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
  fetch('/clear/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         location.href='/';

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });




}

function oneModify(){
  if(!confirm("开始修改了吗?")){
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
  fetch('/modifying/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         var modifyUrl = '/modify/' + value2 + '/';
                         location.href = modifyUrl;

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });




}

function oneAddcontrol(){
  if(!confirm("加入特殊监控?")){
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
  fetch('/addcont/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         var modifyUrl = '/modify/' + value2 + '/';
                         location.href = modifyUrl;

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });




}