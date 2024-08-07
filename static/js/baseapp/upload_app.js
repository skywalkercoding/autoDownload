const uploadapp = document.getElementById('uploadapp');
const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
let isRunning = false;
let loadingText="uploading"
let loadingDots = "";
const maxDots = 3; // 最多显示的点个数
 uploadapp.addEventListener('click', function() {
            isRunning = !isRunning;
            if (isRunning){


                uploadapp.classList.add('disabled');

                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                  const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

             fetch('uploadapp')  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {
                     console.log('data', data)
                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                       uploadapp.classList.remove('disabled')
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         loadingText = "uploading";
                         loadingDots = "";
                         modalBody.textContent = value2;

                       $('#myModal').modal('show');
                    }else{

                       uploadapp.classList.remove('disabled')
                       loadingContainer.style.display = 'none';
                       overlay.style.display = 'none';
                       loadingText = "uploading";
                         loadingDots = "";
                       modalBody.textContent = value2;
                        isRunning=false
                       $('#myModal').modal('show');

                    }

                });

            }

 });

