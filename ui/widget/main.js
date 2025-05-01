document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('opa-form');
    const opaInput = document.getElementById('opa-id');
    const resultsSection = document.getElementById('results');
    const introMessage = document.getElementById('intro-message');
    const introParagraphs = [
      document.getElementById('intro-paragraph1'),
      document.getElementById('intro-paragraph2'),
      document.getElementById('intro-paragraph3'),
      document.getElementById('intro-paragraph4')
    ];
  
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      // Hide intro message
      if (introMessage) {
        introMessage.style.opacity = '0';
        setTimeout(() => {
          introMessage.style.display = 'none';
        }, 20);
      }
  
      // Hide each intro paragraph
      introParagraphs.forEach(p => {
        if (p) {
          p.style.opacity = '0';
          setTimeout(() => {
            p.style.display = 'none';
          }, 20);
        }
      });
  
      const opaId = opaInput.value.trim();
      if (!opaId) {
        resultsSection.innerHTML = '<p>Please enter a valid OPA ID.</p>';
        return;
      }
  
      resultsSection.innerHTML = '<p>Loading assessment history...</p>';
  
      try {
        const response = await fetch('tables-phl_opa_assessment-phl_opa_assessment.jsonl');
        const text = await response.text();
  
        const allLines = text.trim().split('\n');
        const allData = allLines.map(line => JSON.parse(line));
        const filtered = allData
          .filter(entry => entry.parcel_number === opaId)
          .map(entry => ({
            year: parseInt(entry.year),
            value: parseFloat(entry.market_value),
            taxable_land: parseFloat(entry.taxable_land),
            taxable_building: parseFloat(entry.taxable_building),
            exempt_land: parseFloat(entry.exempt_land),
            exempt_building: parseFloat(entry.exempt_building)
          }))
          .sort((a, b) => a.year - b.year);
  
        if (filtered.length === 0) {
          resultsSection.innerHTML = '<p>No data found for that OPA ID.</p>';
          return;
        }
  
        const enriched = filtered.map((item, index, arr) => {
          if (index === 0) return { ...item, change: null, changePct: null };
          const prev = arr[index - 1].value;
          const change = item.value - prev;
          const changePct = (change / prev) * 100;
          return { ...item, change, changePct };
        });
  
        const tableRows = enriched.slice().reverse().map(item => {
          const val = `$${item.value.toLocaleString()}`;
          const delta = item.change == null
            ? '-'
            : `${item.change >= 0 ? '+' : ''}$${item.change.toLocaleString(undefined, { maximumFractionDigits: 0 })} (${item.changePct.toFixed(1)}%)`;
  
          const tl = isNaN(item.taxable_land) ? '-' : `$${item.taxable_land.toLocaleString()}`;
          const tb = isNaN(item.taxable_building) ? '-' : `$${item.taxable_building.toLocaleString()}`;
          const el = isNaN(item.exempt_land) ? '-' : `$${item.exempt_land.toLocaleString()}`;
          const eb = isNaN(item.exempt_building) ? '-' : `$${item.exempt_building.toLocaleString()}`;
  
          return `
            <tr>
              <td>${item.year}</td>
              <td>${val}</td>
              <td>${delta}</td>
              <td>${tl}</td>
              <td>${tb}</td>
              <td>${el}</td>
              <td>${eb}</td>
            </tr>
          `;
        }).join('');
  
        resultsSection.innerHTML = `
          <h2>Valuation History</h2>
          <p>Taxable and exempt land values can represent the contributory value of land in relation to the total market value, or where no structure is present, the value of vacant land. (Consistent with International Association of Assessing Officers (IAAO) standards, the value of an improved parcel is separated into the portion of value attributed to the improvement and the portion of value attributed to the land.)</p>
          <p>To report issues or ask questions regarding your 2025 property assessment, call <a href="tel:2156869200">(215) 686-9200</a> or visit <a href="https://www.phila.gov/opa" target="_blank">www.phila.gov/opa</a>.</p>
          <canvas id="assessmentChart" height="100"></canvas>
          <table>
            <thead>
              <tr>
                <th>Year</th>
                <th>Assessment Value</th>
                <th>Change</th>
                <th>Taxable Land</th>
                <th>Taxable Building</th>
                <th>Exempt Land</th>
                <th>Exempt Building</th>
              </tr>
            </thead>
            <tbody>${tableRows}</tbody>
          </table>
        `;
  
        const ctx = document.getElementById('assessmentChart').getContext('2d');
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: filtered.map(a => a.year),
            datasets: [{
              label: 'Assessment Value',
              data: filtered.map(a => a.value),
              backgroundColor: 'rgba(0, 114, 206, 0.1)',
              borderColor: '#0f4d90',
              borderWidth: 3,
              pointBackgroundColor: '#0f4d90'
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: false,
                ticks: {
                  callback: (value) => '$' + value.toLocaleString(),
                  font: {
                    size: 12,   
                    family: 'Montserrat'
                  }
                },
                grid: {
                  display: false,
                  drawTicks: false
                }
              },
            x: {
              ticks: {
                font: {
                  size: 12,   
                  family: 'Montserrat'
                }
              },
              grid: {
                display: false,
                drawTicks: false
              }
            }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                enabled: true,  // Enable tooltips
                backgroundColor: '#f0f0f0',  // Tooltip background color
                titleColor: '#000000',  // Tooltip title color
                bodyColor: '#000000',  // Tooltip body text color
                borderColor: '#444444',  // Tooltip border color
                borderWidth: 1,  // Tooltip border width
                padding: 12,  // Padding inside the tooltip
                displayColors: false,  // Hide the color box next to the tooltip
                cornerRadius: 1,  // Rounded corners for the tooltip
                xAlign: 'center',  // Align the tooltip horizontally (centered)
                yAlign: 'bottom', 
                titleAlign: 'center',  // <<< Center the title text
                bodyAlign: 'center', // Align the tooltip vertically (above the point)
                callbacks: {
                    label: function(tooltipItem) {
                        return `$${tooltipItem.raw.toLocaleString()}`;  // Format the value in the tooltip
                    },
                title: function(tooltipItem) {
                    return `${tooltipItem[0].label} Assessment`;  // Show year as title
                    }
                }
              }
            }
          }
        });
  
      } catch (error) {
        console.error('Error loading or parsing data:', error);
        resultsSection.innerHTML = '<p class="error">An error occurred. Please try again later.</p>';
      }
    });
  });