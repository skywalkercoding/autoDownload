const overlay = document.getElementById('overlay');
const loadingContainer = document.getElementById('loadingContainer');
const modalBody  = document.getElementById('modalBody');
const showPopupButton = document.getElementById('connectappium');
const delButton = document.getElementById('deleteButton');
//点击next跳到下一步，进行loading加载
        let isRunning = false;
        let loadingText="Connecting"
        let loadingDots = "";
        const maxDots = 3; // 最多显示的点个数
        showPopupButton.addEventListener('click', function() {
            isRunning = !isRunning;
            if (isRunning){


                showPopupButton.classList.add('disabled');
                 showPopupButton.textContent = 'Connecting Appium';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                  const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText + loadingDots;
                loadingDots = loadingDots.length < maxDots ? loadingDots + '.' : '';
            }, 500);

             fetch('connecting')  // 替换成您的后端视图 URL
                .then(response => response.json())
                .then(data => {
                     console.log('data', data)
                    var value1 = data.success;
                    var value2 = data.message;
                    if (value1==true){
                       showPopupButton.textContent = 'Start Installing';
                       loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                        loadingText = "Connecting";
                         loadingDots = "";

                    }else{
                        showPopupButton.textContent = 'Auto Install';
                       showPopupButton.classList.remove('disabled')
                       loadingContainer.style.display = 'none';
                       overlay.style.display = 'none';
                       loadingText = "Connecting";
                         loadingDots = "";

                       modalBody.textContent = value2;
                       isRunning = false;

                       $('#myModal').modal('show');

                    }

                });

            }

 });

        delButton.addEventListener('click' , function(){
              isRunning = !isRunning;
             if (isRunning){

                let loadingText="Deleting"
                delButton.classList.add('disabled');
                 delButton.textContent = 'Deleting';
                 overlay.style.display = 'block';
                 loadingContainer.style.display = 'block';
                 const loadingInterval = setInterval(function() {
                loadingContainer.textContent = loadingText;
                loadingText += ".";

            }, 1000);
               fetch('delete')
                .then(response => response.json())
                .then(data => {
                        console.log('data', data)
                        var value1 = data.success;
                        var value2 = data.message;
                        if (value2==true){
                        loadingContainer.style.display = 'none';
                        overlay.style.display = 'none';
                         delButton.textContent = 'Delete phone App';
                         delButton.classList.remove('disabled');
                         modalBody.textContent = value2;

                       $('#myModal').modal('show');
                        }else{
                           loadingContainer.style.display = 'none';
                          overlay.style.display = 'none';
                          delButton.textContent = 'Delete phone App';
                         delButton.classList.remove('disabled');
                         modalBody.textContent = value2;
                         isRunning = false;

                       $('#myModal').modal('show');

                        };
                });
                }

        });
