
// Get all stars with class of star and turn it into an array
const stars = Array.from(document.querySelectorAll('.stars-inner'));

// Loop through all the classes
stars.forEach(star => {
  // Get star rating within the data attribute value
  const dataRating = star.dataset.rating;
  // total number of stars
  const starTotal = 5;
  // Turn the value into a percentage.
  const starPercentage = `${((dataRating / starTotal) * 100)}%`;
  // Add the percentage value to the class
  star.style.width = starPercentage;
})


