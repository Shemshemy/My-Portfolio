/**
 * BLACKORANGE PORTFOLIO - 3D DEPTH PARALLAX
 * Provides subtle, fluid physics-based mouse parallax for floating cubes & character
 */

(function () {
  'use strict';

  // Check if device is touch-based or prefers reduced motion
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (isTouchDevice || prefersReducedMotion) {
    return; // Don't run mouse parallax on mobile or reduced-motion
  }

  const parallaxElements = document.querySelectorAll('[data-parallax-speed]');
  if (!parallaxElements.length) return;

  let mouseX = 0;
  let mouseY = 0;
  let currentX = 0;
  let currentY = 0;
  const ease = 0.075; // Linear interpolation factor for buttery motion

  // Track window center
  let windowWidth = window.innerWidth;
  let windowHeight = window.innerHeight;

  window.addEventListener('resize', () => {
    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;
  });

  window.addEventListener('mousemove', (e) => {
    // Calculate normalized mouse position from -1 to 1
    mouseX = (e.clientX - windowWidth / 2) / (windowWidth / 2);
    mouseY = (e.clientY - windowHeight / 2) / (windowHeight / 2);
  });

  function updateParallax() {
    // Smooth lerp
    currentX += (mouseX - currentX) * ease;
    currentY += (mouseY - currentY) * ease;

    parallaxElements.forEach((el) => {
      const speed = parseFloat(el.getAttribute('data-parallax-speed')) || 15;
      const rotateSpeed = parseFloat(el.getAttribute('data-parallax-rotate')) || 0;
      
      const translateX = currentX * speed;
      const translateY = currentY * speed;
      const rotate = currentX * rotateSpeed;

      // Combine base CSS translation with parallax offset
      el.style.transform = `translate3d(${translateX}px, ${translateY}px, 0px) rotate(${rotate}deg)`;
    });

    requestAnimationFrame(updateParallax);
  }

  requestAnimationFrame(updateParallax);
})();
