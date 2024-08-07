const excelform = document.getElementById('excelAddForm');
const dwicon = document.getElementById('download_icon');
const crupload = document.getElementById('create_app');
const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
const modalBody  = document.getElementById('modalBody');
var span = document.querySelector('.close');
    let isRunning = false;
        let loadingText="Loading"
        let loadingDots = "";
        const maxDots = 3; // 最多显示的点个数
excelform.addEventListener('submit', async function(e) {

              e.preventDefault();
            const formData = new FormData(excelform);

            const response = await fetch('/1th/upload/', {
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
                isRunning=false
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
  fetch('/1th/clear/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         location.href='/1th/show/';

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                      isRunning=false
                    }

                });




}

function Multidownload(){
    if(!confirm("确定要开始下载?")){
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
  isRunning = !isRunning;
            if (isRunning){
                dwicon.classList.add('disabled');
                 dwicon.textContent = 'Downloading';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

//  location.href='/clear/?id='+str;
  fetch('/1th/dwicon/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         dwicon.classList.remove('disabled');
                        dwicon.textContent = 'Download Icon';

                         location.href='/1th/show/';

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                     dwicon.classList.remove('disabled');
                     dwicon.textContent = 'Download Icon';
                      $('#myModal').modal('show');
                      isRunning=false

                    }

                });

      window.onclick = function(event) {
    if (event.target == modal) {
        modalBody.style.display = "none";
         location.href='/1th/show/';
    }
    // 点击 <span> (x), 关闭弹窗
span.onclick = function() {
       modalBody.style.display = "none";
       location.href='/1th/show/';
}



}

   }
}
function MultiUpload(){
    if(!confirm("确定开始上传?")){
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
  isRunning = !isRunning;
            if (isRunning){
                crupload.classList.add('disabled');
                 crupload.textContent = 'Uploading';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

//  location.href='/clear/?id='+str;
  fetch('/1th/uploadapp/?id='+str)  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         crupload.classList.remove('disabled');
                        crupload.textContent = 'Create App';

                         location.href='/1th/show/';

                    }else{

                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     modalBody.textContent = value2;
                     crupload.classList.remove('disabled');
                     crupload.textContent = 'Create App';
                     isRunning=false
                      $('#myModal').modal('show');

                    }

                });

   }
}