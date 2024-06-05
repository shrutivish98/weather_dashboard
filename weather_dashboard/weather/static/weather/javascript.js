document.addEventListener('DOMContentLoaded', function() {
    createClouds();
});

function createClouds() {
    const numClouds = 2;
    for (let i = 0; i < numClouds; i++) {
        let cloud = document.createElement('div');
        cloud.className = 'clouds';
        cloud.style.top = `${Math.random() * window.innerHeight / 2}px`;
        cloud.style.animationDuration = `${20 + Math.random() * 30}s`;
        document.body.appendChild(cloud);
    }
}