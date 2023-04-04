import os
import streamlit as st
from PIL import Image, ImageDraw

def main():
    st.title("image_crop.py")
    
    # ファイルアップロード
    uploaded_file = st.file_uploader("写真をアップロード", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # アップロードされたファイルを読み込む
        image = Image.open(uploaded_file)
        # プレビュー用
        image_preview = image.copy()
        # 切り抜き用
        image_cropped = image.copy()
        
        # 画像サイズの取得
        width, height = image.size
        
        # 画像を表示
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # 切り抜きの形状を選択
        shape = st.radio("切り抜く形状を選択してください", ("円形", "矩形"))

        # 切り抜き用マスク生成
        mask = Image.new("L", image.size, 0)
        draw_mask = ImageDraw.Draw(mask)

        # プレビュー用マスク生成
        preview_pixel_value = 70
        mask_preview = Image.new("L", image.size, preview_pixel_value)
        draw_mask_preview = ImageDraw.Draw(mask_preview)

        # 切り抜き領域の指定
        st.sidebar.write("パラメータの設定")
        if shape == "円形":
            # 切り抜き領域の座標を取得
            radius = st.sidebar.slider("半径", 1, min(width, height)//2 - 1, 100)
            center_x = st.sidebar.slider("中心座標（横）", radius, width - radius, radius)
            center_y = st.sidebar.slider("中心座標（縦）", radius, height - radius, radius)

            # マスクの生成
            left, right = center_x - radius, center_x + radius
            top, bottom = center_y - radius, center_y + radius
            draw_mask.ellipse((left, top, right, bottom), fill=255)
            draw_mask_preview.ellipse((left, top, right, bottom), fill=255)

        elif shape == "矩形":
            # 切り抜き領域の座標を取得
            left, right = st.sidebar.slider("横（左端，右端）", 0, width, (0, width), 1)
            top, bottom = st.sidebar.slider("縦（上端，下端）", 0, height, (0, height), 1)

            # マスクの生成
            draw_mask.rectangle((left, top, right, bottom), fill=255)
            draw_mask_preview.rectangle((left, top, right, bottom), fill=255)

        else:
            st.error('今のところ矩形か円形しか対応してないよ', icon="🚨")

        # マスクの適用
        image_cropped.putalpha(mask)
        image_cropped = image_cropped.crop((left, top, right, bottom))
        image_preview.putalpha(mask_preview)
        
        # プレビューの表示
        st.image(image_preview, caption="Cropped Image", use_column_width=True)
        
        # 切り抜き画像を保存
        save_button = st.button("保存")
        if save_button:
            saveDir = "./dst/"
            imgName = uploaded_file.name.split(".")[0]
            # 保存用フォルダがない場合は生成
            if not os.path.exists(saveDir): 
                os.makedirs(saveDir)
            else:
                pass
            
            image_cropped.save(f"{saveDir}{imgName}_cropped.png")
            st.success("切り抜き画像を保存しました")

if __name__ == '__main__':
    main()
