/* ==================================================
   전역 변수
================================================== */

// 현재 수정 중인 포트폴리오 ID
let editingId = null;


// 현재 선택된 카테고리
let currentCategory = "all";


// 선택한 파일
let selectedFile = null;



/* ==================================================
   HTML 요소 가져오기
================================================== */

const titleInput =
    document.getElementById("titleInput");


const categoryInput =
    document.getElementById("categoryInput");


const descriptionInput =
    document.getElementById("descriptionInput");


const fileInput =
    document.getElementById("fileInput");


const previewContainer =
    document.getElementById("previewContainer");


const saveButton =
    document.getElementById("saveButton");


const cancelButton =
    document.getElementById("cancelButton");


const portfolioGrid =
    document.getElementById("portfolioGrid");


const emptyMessage =
    document.getElementById("emptyMessage");


const searchInput =
    document.getElementById("searchInput");


const dropZone =
    document.getElementById("dropZone");


const detailModal =
    document.getElementById("detailModal");


const detailContent =
    document.getElementById("detailContent");


const closeModal =
    document.getElementById("closeModal");


const openUploadButton =
    document.getElementById("openUploadButton");



/* ==================================================
   포트폴리오 데이터 가져오기
================================================== */

function getPortfolios() {

    const data =
        localStorage.getItem(
            "myPortfolios"
        );


    if (!data) {

        return [];

    }


    return JSON.parse(data);
}



/* ==================================================
   포트폴리오 저장
================================================== */

function savePortfolios(portfolios) {

    localStorage.setItem(

        "myPortfolios",

        JSON.stringify(portfolios)

    );

}



/* ==================================================
   파일 선택
================================================== */

fileInput.addEventListener(
    "change",
    function () {

        const file =
            fileInput.files[0];


        if (!file) {

            return;

        }


        selectedFile = file;


        createPreview(file);

    }
);



/* ==================================================
   썸네일 생성
================================================== */

function createPreview(file) {

    previewContainer.innerHTML = "";


    const previewCard =
        document.createElement("div");


    previewCard.className =
        "preview-card";


    // 이미지 파일
    if (
        file.type.startsWith("image/")
    ) {

        const image =
            document.createElement("img");


        image.className =
            "preview-image";


        image.src =
            URL.createObjectURL(file);


        previewCard.appendChild(image);

    }


    // 이미지가 아닌 파일
    else {

        const icon =
            document.createElement("div");


        icon.className =
            "preview-image";


        icon.style.display =
            "flex";


        icon.style.alignItems =
            "center";


        icon.style.justifyContent =
            "center";


        icon.style.fontSize =
            "35px";


        icon.textContent =
            getFileIcon(file.type);


        previewCard.appendChild(icon);

    }


    const fileName =
        document.createElement("div");


    fileName.innerHTML = `

        <strong>
            ${file.name}
        </strong>

        <br>

        <small>
            ${formatFileSize(file.size)}
        </small>

    `;


    previewCard.appendChild(fileName);


    previewContainer.appendChild(
        previewCard
    );

}



/* ==================================================
   파일 아이콘
================================================== */

function getFileIcon(type) {

    if (
        type.includes("pdf")
    ) {

        return "📕";

    }


    if (
        type.includes("video")
    ) {

        return "🎬";

    }


    if (
        type.includes("html")
    ) {

        return "🌐";

    }


    if (
        type.includes("word")
    ) {

        return "📘";

    }


    return "📄";
}



/* ==================================================
   파일 크기
================================================== */

function formatFileSize(size) {

    if (size < 1024) {

        return size + " B";

    }


    if (size < 1024 * 1024) {

        return (
            (size / 1024).toFixed(1)
            + " KB"
        );

    }


    return (
        (size / (1024 * 1024)).toFixed(1)
        + " MB"
    );

}



/* ==================================================
   이미지 파일을 Data URL로 변환
================================================== */

function fileToDataURL(file) {

    return new Promise(
        function (resolve, reject) {

            const reader =
                new FileReader();


            reader.onload =
                function () {

                    resolve(
                        reader.result
                    );

                };


            reader.onerror =
                function () {

                    reject(
                        reader.error
                    );

                };


            reader.readAsDataURL(file);

        }
    );

}



/* ==================================================
   포트폴리오 등록
================================================== */

saveButton.addEventListener(
    "click",
    async function () {

        const title =
            titleInput.value.trim();


        const category =
            categoryInput.value;


        const description =
            descriptionInput.value.trim();


        // 제목 검사
        if (!title) {

            alert(
                "포트폴리오 제목을 입력하세요."
            );

            titleInput.focus();

            return;
        }


        // 설명 검사
        if (!description) {

            alert(
                "포트폴리오 설명을 입력하세요."
            );

            descriptionInput.focus();

            return;
        }



        /* ==========================================
           수정
        ========================================== */

        if (editingId) {

            updatePortfolio(

                editingId,

                title,

                category,

                description

            );

            return;
        }



        /* ==========================================
           신규 등록
        ========================================== */

        if (!selectedFile) {

            alert(
                "과제물 파일을 선택하세요."
            );

            return;

        }



        // 파일을 Data URL로 변환
        let fileData = "";

        try {

            fileData =
                await fileToDataURL(
                    selectedFile
                );

        }

        catch (error) {

            alert(
                "파일을 읽을 수 없습니다."
            );

            return;

        }



        const portfolio = {

            id:
                Date.now(),

            title:
                title,

            category:
                category,

            description:
                description,

            fileName:
                selectedFile.name,

            fileType:
                selectedFile.type,

            fileSize:
                selectedFile.size,

            fileData:
                fileData,

            createdAt:
                new Date()
                    .toLocaleDateString(
                        "ko-KR"
                    )

        };



        const portfolios =
            getPortfolios();


        portfolios.unshift(
            portfolio
        );


        savePortfolios(
            portfolios
        );


        alert(
            "포트폴리오가 등록되었습니다!"
        );


        resetForm();


        renderPortfolios();


        // 포트폴리오 영역으로 이동
        document
            .getElementById("portfolio")
            .scrollIntoView({
                behavior: "smooth"
            });

    }
);



/* ==================================================
   포트폴리오 화면 출력
================================================== */

function renderPortfolios() {

    const portfolios =
        getPortfolios();


    const keyword =
        searchInput.value
            .trim()
            .toLowerCase();



    portfolioGrid.innerHTML =
        "";



    let filtered =
        portfolios.filter(
            function (portfolio) {


                // 카테고리 필터
                const categoryMatch =

                    currentCategory ===
                    "all"

                    ||

                    portfolio.category ===
                    currentCategory;



                // 검색 필터
                const searchMatch =

                    portfolio.title
                        .toLowerCase()
                        .includes(keyword)

                    ||

                    portfolio.description
                        .toLowerCase()
                        .includes(keyword);



                return (
                    categoryMatch
                    &&
                    searchMatch
                );

            }
        );



    // 결과가 없는 경우
    if (filtered.length === 0) {

        emptyMessage.style.display =
            "block";

        return;

    }


    emptyMessage.style.display =
        "none";



    // 카드 생성
    filtered.forEach(
        function (portfolio) {

            createPortfolioCard(
                portfolio
            );

        }
    );

}



/* ==================================================
   포트폴리오 카드 생성
================================================== */

function createPortfolioCard(
    portfolio
) {

    const card =
        document.createElement(
            "article"
        );


    card.className =
        "portfolio-card";



    /* ==========================================
       썸네일
    ========================================== */

    const imageArea =
        document.createElement(
            "div"
        );


    imageArea.className =
        "card-image";



    // 이미지 파일
    if (
        portfolio.fileType.startsWith(
            "image/"
        )
    ) {

        const image =
            document.createElement(
                "img"
            );


        image.src =
            portfolio.fileData;


        imageArea.appendChild(
            image
        );

    }


    // 기타 파일
    else {

        const icon =
            document.createElement(
                "div"
            );


        icon.className =
            "file-icon";


        icon.textContent =
            getFileIcon(
                portfolio.fileType
            );


        imageArea.appendChild(
            icon
        );

    }



    /* ==========================================
       카드 내용
    ========================================== */

    const content =
        document.createElement(
            "div"
        );


    content.className =
        "card-content";


    content.innerHTML = `

        <span class="card-category">

            ${getCategoryName(
                portfolio.category
            )}

        </span>


        <h3>
            ${escapeHTML(
                portfolio.title
            )}
        </h3>


        <p>

            ${escapeHTML(
                portfolio.description
            )}

        </p>


        <div class="card-footer">

            <span class="card-date">

                ${portfolio.createdAt}

            </span>


            <div class="card-actions">

                <button
                    class="view-button">

                    보기

                </button>


                <button
                    class="edit-button">

                    수정

                </button>


                <button
                    class="delete-button">

                    삭제

                </button>

            </div>

        </div>

    `;



    /* ==========================================
       카드 조립
    ========================================== */

    card.appendChild(
        imageArea
    );


    card.appendChild(
        content
    );


    portfolioGrid.appendChild(
        card
    );



    /* ==========================================
       보기
    ========================================== */

    card
        .querySelector(
            ".view-button"
        )
        .addEventListener(
            "click",
            function () {

                showDetail(
                    portfolio.id
                );

            }
        );



    /* ==========================================
       수정
    ========================================== */

    card
        .querySelector(
            ".edit-button"
        )
        .addEventListener(
            "click",
            function () {

                editPortfolio(
                    portfolio.id
                );

            }
        );



    /* ==========================================
       삭제
    ========================================== */

    card
        .querySelector(
            ".delete-button"
        )
        .addEventListener(
            "click",
            function () {

                deletePortfolio(
                    portfolio.id
                );

            }
        );

}



/* ==================================================
   카테고리 이름
================================================== */

function getCategoryName(
    category
) {

    const names = {

        html: "HTML",

        image: "IMAGE",

        video: "VIDEO",

        document: "DOCUMENT",

        other: "OTHER"

    };


    return names[category]
        || "OTHER";

}



/* ==================================================
   상세 페이지
================================================== */

function showDetail(id) {

    const portfolios =
        getPortfolios();


    const portfolio =
        portfolios.find(
            function (item) {

                return item.id === id;

            }
        );


    if (!portfolio) {

        return;

    }



    let mediaHTML = "";



    // 이미지
    if (
        portfolio.fileType.startsWith(
            "image/"
        )
    ) {

        mediaHTML = `

            <img
                class="detail-image"
                src="${portfolio.fileData}">

        `;

    }



    // 영상
    else if (
        portfolio.fileType.startsWith(
            "video/"
        )
    ) {

        mediaHTML = `

            <video
                class="detail-image"
                controls>

                <source
                    src="${portfolio.fileData}"
                    type="${portfolio.fileType}">

            </video>

        `;

    }



    // 기타
    else {

        mediaHTML = `

            <div class="detail-file">

                📄

                ${escapeHTML(
                    portfolio.fileName
                )}

            </div>

        `;

    }



    detailContent.innerHTML = `

        ${mediaHTML}


        <div class="detail-category">

            ${getCategoryName(
                portfolio.category
            )}

        </div>


        <h2 class="detail-title">

            ${escapeHTML(
                portfolio.title
            )}

        </h2>


        <p class="detail-description">

            ${escapeHTML(
                portfolio.description
            )}

        </p>


        <div class="detail-file">

            파일명 :

            ${escapeHTML(
                portfolio.fileName
            )}

            <br>

            크기 :

            ${formatFileSize(
                portfolio.fileSize
            )}

        </div>

    `;


    detailModal.classList.add(
        "show"
    );

}



/* ==================================================
   상세 모달 닫기
================================================== */

closeModal.addEventListener(
    "click",
    function () {

        detailModal.classList.remove(
            "show"
        );

    }
);



/* 바깥 영역 클릭 */

detailModal.addEventListener(
    "click",
    function (event) {

        if (
            event.target ===
            detailModal
        ) {

            detailModal.classList.remove(
                "show"
            );

        }

    }
);



/* ==================================================
   수정
================================================== */

function editPortfolio(id) {

    const portfolios =
        getPortfolios();


    const portfolio =
        portfolios.find(
            function (item) {

                return item.id === id;

            }
        );


    if (!portfolio) {

        return;

    }



    // 수정 ID 저장
    editingId =
        id;


    // 기존 데이터 입력
    titleInput.value =
        portfolio.title;


    categoryInput.value =
        portfolio.category;


    descriptionInput.value =
        portfolio.description;



    // 버튼 이름 변경
    saveButton.textContent =
        "포트폴리오 수정";


    // 업로드 영역으로 이동
    document
        .getElementById("upload")
        .scrollIntoView({
            behavior: "smooth"
        });

}



/* ==================================================
   수정 저장
================================================== */

function updatePortfolio(
    id,
    title,
    category,
    description
) {

    const portfolios =
        getPortfolios();


    const index =
        portfolios.findIndex(
            function (item) {

                return item.id === id;

            }
        );


    if (index === -1) {

        return;

    }



    portfolios[index].title =
        title;


    portfolios[index].category =
        category;


    portfolios[index].description =
        description;


    savePortfolios(
        portfolios
    );


    alert(
        "포트폴리오가 수정되었습니다."
    );


    resetForm();


    renderPortfolios();

}



/* ==================================================
   삭제
================================================== */

function deletePortfolio(id) {

    const answer =
        confirm(
            "정말 삭제하시겠습니까?"
        );


    if (!answer) {

        return;

    }


    let portfolios =
        getPortfolios();


    portfolios =
        portfolios.filter(
            function (item) {

                return item.id !== id;

            }
        );


    savePortfolios(
        portfolios
    );


    renderPortfolios();


    alert(
        "삭제되었습니다."
    );

}



/* ==================================================
   검색
================================================== */

searchInput.addEventListener(
    "input",
    function () {

        renderPortfolios();

    }
);



/* ==================================================
   카테고리
================================================== */

const categoryButtons =
    document.querySelectorAll(
        ".category-button"
    );


categoryButtons.forEach(
    function (button) {

        button.addEventListener(
            "click",
            function () {

                currentCategory =
                    button.dataset.category;


                categoryButtons.forEach(
                    function (item) {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                button.classList.add(
                    "active"
                );


                renderPortfolios();

            }
        );

    }
);



/* ==================================================
   등록 영역 열기
================================================== */

openUploadButton.addEventListener(
    "click",
    function () {

        document
            .getElementById("upload")
            .scrollIntoView({
                behavior: "smooth"
            });

    }
);



/* ==================================================
   취소
================================================== */

cancelButton.addEventListener(
    "click",
    function () {

        resetForm();

    }
);



/* ==================================================
   폼 초기화
================================================== */

function resetForm() {

    titleInput.value =
        "";


    categoryInput.value =
        "html";


    descriptionInput.value =
        "";


    fileInput.value =
        "";


    previewContainer.innerHTML =
        "";


    selectedFile =
        null;


    editingId =
        null;


    saveButton.textContent =
        "포트폴리오 등록";

}



/* ==================================================
   드래그 앤 드롭
================================================== */

dropZone.addEventListener(
    "dragover",
    function (event) {

        event.preventDefault();


        dropZone.classList.add(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "dragleave",
    function () {

        dropZone.classList.remove(
            "dragover"
        );

    }
);


dropZone.addEventListener(
    "drop",
    function (event) {

        event.preventDefault();


        dropZone.classList.remove(
            "dragover"
        );


        const file =
            event.dataTransfer.files[0];


        if (!file) {

            return;

        }


        selectedFile =
            file;


        createPreview(file);

    }
);



/* ==================================================
   HTML 특수문자 방지
================================================== */

function escapeHTML(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;

}



/* ==================================================
   페이지 시작
================================================== */

renderPortfolios();