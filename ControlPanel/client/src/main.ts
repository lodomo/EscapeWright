import './output.css'
import ewSettings from './ew_settings.ts'

document.querySelector<HTMLDivElement>('title')!.innerText = ewSettings.title

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    ${Object.entries(ewSettings).map(([key, value]) => `<p><strong>${key}:</strong> ${value}</p>`).join('')};
  </div>
`
