type AnnotData = {
  seq: number
  label: number
}[]

document.getElementById("annot-btn")?.addEventListener("click", () => {
  const form = document.getElementById("form")
  if (form) {
    const data: AnnotData = []
    new FormData(form as HTMLFormElement).forEach((v, k) => {
      data.push({seq: parseInt(k), label: parseInt(v as string)})
    })
    fetch("/label", {body: JSON.stringify(data), headers: {"Content-Type": "application/json"}, method: "PUT"})
  }
})
