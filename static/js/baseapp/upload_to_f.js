const modalBody  = document.getElementById('modalBody');
const uploadFApp  = document.getElementById('upload_f_app');
let isRunning = false;
let loadingDots = "";
let loadingText="Logining"
const maxDots = 3; // 最多显示的点个数
uploadFApp.addEventListener('click', function() {
            isRunning = !isRunning;
            if (isRunning){
                uploadFApp.classList.add('disabled');
                 uploadFApp.textContent = 'Stop';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

             fetch('/3th/loginf/')  // 替换成您的后端视图 URL
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

                    }else{
                     uploadFApp.classList.remove('disabled');
                     uploadFApp.textContent = 'Run';
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


//upload 删除语句
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
  fetch('/3th/deldownload/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');

                          location.href='/3th/upload';

                    }else{

                        modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });




}