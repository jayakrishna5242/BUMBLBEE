window.addEventListener("load", canvasApp, false);

var sphereRad = 140;
var radius_sp = 1;
var canvas, ctx, particles = [];
var fLen = 320; // Focal length
var projCenterX, projCenterY;
var turnAngle = 0;
var turnSpeed = Math.PI / 2000; // SLOWER ROTATION SPEED
var gravity = 0.0005; // REDUCE GRAVITY FOR SLOWER MOVEMENT
var particleRad = 2;
var numParticles = 500;
var glowIntensity = 20; // Default glow intensity
var glowColor = "rgba(0, 72, 255, 0.8)"; // Glow color for particles
var edgeGlowColor = "rgba(0, 72, 255, 0.5)"; // Glow color for sphere edge
var initTextTimeout; // Variable to store the timeout for initialization text

function canvasApp() {
    canvas = document.getElementById("canvasOne");
    ctx = canvas.getContext("2d");

    projCenterX = canvas.width / 2;
    projCenterY = canvas.height / 2;

    initParticles();
    requestAnimationFrame(updateFrame);

    // Hide the initialization text after 10 seconds
    initTextTimeout = setTimeout(function () {
        document.getElementById("init-text").style.visibility = "hidden";
    }, 10000);

    // Slider for Sphere Radius
    $("#slider-range").slider({
        range: false,
        min: 50,
        max: 500,
        value: 140,
        slide: function (event, ui) {
            sphereRad = ui.value;
            initParticles(); // Reinitialize particles when sphere radius changes
        }
    });

    // Slider for Particle Size
    $("#slider-test").slider({
        range: false,
        min: 0.5,
        max: 2.5,
        value: 1,
        step: 0.01,
        slide: function (event, ui) {
            radius_sp = ui.value;
        }
    });

    // Slider for Glow Intensity
    $("#slider-glow").slider({
        range: false,
        min: 0,
        max: 50,
        value: 20,
        slide: function (event, ui) {
            glowIntensity = ui.value;
        }
    });
}

function initParticles() {
    particles = []; // Reset particles array
    for (let i = 0; i < numParticles; i++) {
        let theta = Math.random() * Math.PI * 2;
        let phi = Math.acos(Math.random() * 2 - 1);
        let x0 = sphereRad * Math.sin(phi) * Math.cos(theta);
        let y0 = sphereRad * Math.sin(phi) * Math.sin(theta);
        let z0 = sphereRad * Math.cos(phi);

        particles.push({
            x: x0, y: y0, z: z0,
            velX: 0.0005 * x0, // LOWER VALUE FOR SLOWER PARTICLE SPEED
            velY: 0.0005 * y0,
            velZ: 0.0005 * z0,
            alpha: 1,
            stuckTime: 50 + Math.random() * 30
        });
    }
}

function updateFrame() {
    turnAngle += turnSpeed;
    let sinA = Math.sin(turnAngle);
    let cosA = Math.cos(turnAngle);

    // Clear the canvas with a semi-transparent black background for a trailing effect
    ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw the glowing edge effect around the sphere
    ctx.shadowBlur = glowIntensity * 2; // Increase the blur for a bigger glow
    ctx.shadowColor = edgeGlowColor; // Soft blue glow for edges
    ctx.strokeStyle = edgeGlowColor; // Soft blue stroke for edge glow
    ctx.lineWidth = 5; // Edge width for better visibility

    // Draw the outer glow effect (a circle at the center with the sphere radius)
    ctx.beginPath();
    ctx.arc(projCenterX, projCenterY, sphereRad * fLen / (fLen - 100), 0, Math.PI * 2);
    ctx.stroke(); // Outline with glow effect
    ctx.shadowBlur = 0; // Reset shadow after drawing the edge glow

    // Enable glowing effect for particles
    ctx.shadowBlur = glowIntensity; // Adjust the blur radius for particles' glow
    ctx.shadowColor = glowColor; // Glow color (matches particle color)

    particles.forEach(p => {
        p.stuckTime--;
        if (p.stuckTime < 0) {
            p.velY += gravity; // Apply gravity
            p.x += p.velX;
            p.y += p.velY;
            p.z += p.velZ;
        }

        // Apply the same rotation to particles
        let rotX = cosA * p.x + sinA * p.z;
        let rotZ = -sinA * p.x + cosA * p.z;
        let scale = radius_sp * fLen / (fLen - rotZ);
        let projX = rotX * scale + projCenterX;
        let projY = p.y * scale + projCenterY;

        // Dynamic glow intensity based on particle depth (z-position)
        let depthGlow = Math.max(0, 1 - p.z / fLen); // Glow fades as particles move away
        ctx.shadowBlur = glowIntensity * depthGlow;

        // Draw the particle with a glowing effect
        ctx.fillStyle = `rgba(0, 72, 255, ${p.alpha})`;
        ctx.beginPath();
        ctx.arc(projX, projY, particleRad * scale, 0, Math.PI * 2);
        ctx.fill();
    });

    // Disable glowing effect for other elements (if any)
    ctx.shadowBlur = 0;
    ctx.shadowColor = "transparent";

    requestAnimationFrame(updateFrame);
}
