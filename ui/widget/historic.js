document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('opa-form');
  const opaInput = document.getElementById('opa-id');
  const resultsSection = document.getElementById('results');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const opaId = opaInput.value.trim();
    if (!opaId) {
      resultsSection.innerHTML = '<p>Please enter a valid OPA ID.</p>';
      return;
    }

    resultsSection.innerHTML = '<p>Loading assessment history...</p>';

    try {
      // Simulate fetch delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Example assessment history
      let assessments = [
        { year: 2024, value: 210000 },
        { year: 2022, value: 195000 },
        { year: 2023, value: 200000 },
        { year: 2021, value: 190000 }
      ];

      // Sort assessments ascending for the graph (oldest first)
      const assessmentsForGraph = [...assessments].sort((a, b) => a.year - b.year);

      // Sort assessments descending for the table (newest first)
      const assessmentsForTable = [...assessments].sort((a, b) => b.year - a.year);

      // Clear and build new content
      resultsSection.innerHTML = `
        <h2>Valuation History</h2>
        <p>Taxable and exempt land values can represent the contributory value of land in relation to the total market value, or where no structure is present, the value of vacant land. (Consistent with International Association of Assessing Officers (IAAO) standards, the value of an improved parcel is separated into the portion of value attributed to the improvement and the portion of value attributed to the land.)</p>
        <p>To report issues or ask questions regarding your 2025 property assessment, call <a href="tel:2156869200">(215) 686-9200</a>  or visit <a href="https://www.phila.gov/opa" target="_blank">www.phila.gov/opa</a>.</p>

        <canvas id="assessmentChart"></canvas>

        <table>
          <thead>
            <tr><th>Year</th><th>Assessment Value</th></tr>
          </thead>
          <tbody>
            ${assessmentsForTable.map(a => `<tr><td>${a.year}</td><td>$${a.value.toLocaleString()}</td></tr>`).join('')}
          </tbody>
        </table>
      `;

      // Draw chart
      const ctx = document.getElementById('assessmentChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: assessmentsForGraph.map(a => a.year),
          datasets: [{
            label: 'Assessment Value',
            data: assessmentsForGraph.map(a => a.value),
            backgroundColor: 'rgba(0, 114, 206, 0.1)',
            borderColor: '#0072ce',
            borderWidth: 2,
            pointBackgroundColor: '#0072ce'
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: (value) => '$' + value.toLocaleString()
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });

    } catch (error) {
      console.error(error);
      resultsSection.innerHTML = '<p class="error">An error occurred. Please try again later.</p>';
    }
  });
});