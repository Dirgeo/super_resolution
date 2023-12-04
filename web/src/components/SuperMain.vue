<template>

    <div style="margin-top: 20px;">

      <!-- page header-->
    <div class="page-header d-print-none">
      <div class="container-xl">
        <div class="row g-2 align-items-center">

          <div class="col">
            <h2 class="page-title">
              创建检测任务
            </h2>
            <div class="text-muted mt-1">
              选择图片上传即可！<br>
              仅作为模型Demo使用，图片通道要求为3，分辨率不得大于500*500
            </div>
          </div>

        </div>
      </div>
    </div>



    <div class="page-body">

      <div class="container-xl">

        <div class="card">
          <div class="container">
            <div class="row row-cards justify-content-center">
              <!-- 头部标题 -->
              <div class="col-12 card-header">
                图像超分

                <div class="row row-cards justify-content-center">
                  <div class="col-6">
                    <input v-if='mode === 0' @change="getFile($event)" type="file" class="form-control" id="inputGroupFile04" aria-describedby="inputGroupFileAddon04" aria-label="Upload">
                    <button v-else type="button" class="btn btn-success"  @click="start_shot">开始拍摄</button>
                  </div>
                  <div class="col-3" v-if='!$store.state.model.running'>
                    <button type="button" class="btn btn-success"  @click="sr()">开始超分处理</button>
                  </div>
                  <div class="col-2" v-if='!$store.state.model.running'>
                    <button type="button" class="btn btn-success"  @click="switch_mode">切换模式</button>
                  </div>
                  <div v-else class="col-6 spinner-border text-success" role="status" >
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>

                <div class="row row-cards justify-content-end">
                  <div class="col-4 card-text"></div>
                  <div class="col-4 card-text"></div>
                  <div class="col-4 card-text"></div>
                </div>

              </div>

              <div class="row card-body justify-content-center">
                <!-- 源图片区域 -->
                <div class="col-6 photo-area card border border-dark border-2" style="margin-right: 20px;padding: 0;">
                  <img class="card-img img-thumbnail" :src="$store.state.model.source_image" style="width: 100%;height: 100%;">
                  <!-- <div class="d-flex justify-content-center carousel-caption d-none d-md-block">
                    <h5>选择上传的图片</h5>
                    <p class="fs-1">点击下方按钮选择要上传的图片.</p>
                  </div> -->
                </div>
                <!-- 推理后图片区域 -->
                <div class="col-6 photo-area card border border-dark border-2 d-flex" style="margin-left: 20px;padding: 0;">
                  <img class="card-img img-thumbnail" :src="$store.state.model.target_image" style="width: 100%;height: 100%;">
                  <!-- <div class="d-flex justify-content-center carousel-caption d-none d-md-block">
                    <h5>检测后的图片</h5>
                    <p class="fs-1">点击下方按钮开始检测.</p>
                  </div> -->
                </div>

              </div>

            </div>
          </div>
        </div>

      </div>

    </div>

    </div>

</template>

<script>
import {useStore} from "vuex";
import $ from "jquery";
import {ref} from "vue";

export default {
  name: "SuperMain.vue",
  components:{
  },
  setup(){

    const store = useStore()

    let choose_image = null
    let b64 = "";// 图片的base64编码

    const getFile = (e)=>{
      choose_image = e.target.files[0]
      // 检查上传文件的类型
      if(choose_image !== null && choose_image.type.indexOf("image") === -1){
        choose_image = null
        alert("传什么呢!!!")
      }

      const reader = new FileReader()

      reader.onload = (file)=>{
        // 得到url安全的base64
        b64 = file.target.result.split(",")[1]
        // b64 = b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "")
        let image = {
          source_image: file.target.result,
          target_image: null,
        }
        store.commit("updateImage", image)
      }

      reader.readAsDataURL(choose_image)
    }

    const sr = ()=>{
      store.commit("updateRunning", true)
      // 使用base64编码
      console.log("start send https")
      $.ajax({
        url: "https://lovespace.club/edsr/",
        type:'post',
        data:{
          source:b64,
        },
        success(res){
          if(res.state === "success"){
            let target_image = "data:image/png;base64," + res.data
            store.commit("updateImage", {
              source_image: store.state.model.source_image,
              target_image: target_image,
            })
          } else {
            alert(res.data)
          }
          store.commit("updateRunning", false)
        },
        error(){
          alert("请求失败，稍后再试")
          store.commit("updateRunning", false)
        }
      })

    }

    let mode = ref(0) // 0代表选择图片模式，1代表拍摄模式

    const switch_mode = ()=>{
      mode.value = mode.value^1
    }

    const start_shot = ()=>{
      
    }

    return {
      getFile,
      sr,
      mode,
      switch_mode,
      start_shot,
    }
  }
}
</script>

<style scoped>
div.photo-area{
  width: 45%;
  height: 60vh;
  background-color: rgba(200,200,200);
  justify-content: center;
  align-content: center;
}
div.photo-area>img{
  width: 100%;
  height: 100%;
}
</style>