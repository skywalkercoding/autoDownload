const showPopupButton = document.getElementById('nextDownloadButton');
const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
const modalBody  = document.getElementById('modalBody');

//点击next跳到下一步，进行loading加载
        let isRunning = false;
        let loadingText="Loading"
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

             fetch('/downloading')  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {

                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                          modalBody.textContent = value2;
                           $('#myModal').modal('show');
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         loadingText = "Loading";
                         loadingDots = "";
                       window.location.href = '/2th/download';   // 跳转到目标页面
                    }else{
                     showPopupButton.classList.remove('disabled');
                     showPopupButton.textContent = 'Run';
                     loadingContainer.style.display = 'none';
                     overlay.style.display = 'none';
                     loadingText = "Loading";
                       loadingDots = "";
                       isRunning = false;
                     modalBody.textContent = value2;
                      $('#myModal').modal('show');
                    }

                });

            }

 });

