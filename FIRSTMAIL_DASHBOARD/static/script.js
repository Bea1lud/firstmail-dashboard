document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (form) {

        form.addEventListener("submit", () => {

            const button = document.querySelector(
                ".submit-btn"
            );

            if (button) {

                button.disabled = true;

                button.textContent =
                    "Проверяем аккаунты...";
            }

        });

    }

    const codeCells = document.querySelectorAll(
        ".code-cell"
    );

    codeCells.forEach((cell) => {

        cell.style.cursor = "pointer";

        cell.addEventListener(
            "click",
            async () => {

                const code =
                    cell.textContent.trim();

                if (
                    !code ||
                    code === "—"
                ) {
                    return;
                }

                try {

                    await navigator.clipboard.writeText(
                        code
                    );

                    showNotification(
                        `Код ${code} скопирован`
                    );

                } catch (error) {

                    console.error(error);

                }

            }
        );

    });

});


function showNotification(text) {

    const oldNotification =
        document.querySelector(
            ".notification"
        );

    if (oldNotification) {
        oldNotification.remove();
    }

    const notification =
        document.createElement("div");

    notification.className =
        "notification";

    notification.textContent =
        text;

    document.body.appendChild(
        notification
    );

    setTimeout(() => {

        notification.classList.add(
            "show"
        );

    }, 10);

    setTimeout(() => {

        notification.classList.remove(
            "show"
        );

        setTimeout(() => {

            notification.remove();

        }, 300);

    }, 2000);

}