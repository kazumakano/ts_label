document.getElementById("export-btn")?.addEventListener("click", () => {
  fetch("/dataset").then(res => {
    if (res.ok) alert("Exported")
  })
})

type Data = {
  seq: number
  label: number
}[]

document.getElementById("label-btn")?.addEventListener("click", () => {
  const form = document.getElementById("form")
  if (form) {
    const data: Data = []
    new FormData(form as HTMLFormElement).forEach((v, k) => {
      data.push({seq: parseInt(k), label: parseInt(v as string)})
    })
    fetch("/label", {body: JSON.stringify(data), headers: {"Content-Type": "application/json"}, method: "PATCH"}).then(res => {
      if (res.ok) window.location.reload()
    })
  }
})

document.getElementById("scan-btn")?.addEventListener("click", () => {
  window.location.href = "/"
})
